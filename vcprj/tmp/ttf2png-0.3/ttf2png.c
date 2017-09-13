/*
ttf2png - True Type Font to PNG converter
Copyright (c) 2004-2008 Mikko Rasa

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
*/

#include <stdio.h>
#include <ctype.h>
#include <unistd.h>
#include <getopt.h>
#include <png.h>
#include <ft2build.h>
#include FT_FREETYPE_H

typedef struct sImage
{
	unsigned w, h;
	char     *data;
} Image;

typedef struct sGlyph
{
	unsigned code;
	Image    image;
	unsigned x, y;
	int      offset_x;
	int      offset_y;
	int      advance;
} Glyph;

typedef struct sFont
{
	unsigned size;
	int      ascent;
	int      descent;
	unsigned n_glyphs;
	Glyph    *glyphs;
	Image    image;
} Font;

unsigned round_to_pot(unsigned);
void usage();
void init_font(Font *, FT_Face, unsigned, unsigned, int);
void render_grid(Font *, unsigned, unsigned, int);
void render_packed(Font *);
int save_defs(const char *, const Font *);
int save_png(const char *, const Image *, char);

char verbose=0;

int main(int argc, char **argv)
{
	char *fn;
	int  begin=0;
	int  end=255;
	int  size=10;
	int  cpl=0;
	int  cell=0;
	char autohinter=0;
	char seq=0;
	char alpha=0;
	char pack=0;

	FT_Library freetype;
	FT_Face    face;

	int  err;
	int  i;

	char *out_fn="font.png";

	char *def_fn=NULL;

	Font font;

	if(argc<2)
	{
		usage();
		return 1;
	}

	while((i=getopt(argc, argv, "r:s:l:c:o:atvh?ed:p"))!=-1)
	{
		char *ptr;
		int  temp;
		switch(i)
		{
		case 'r':
			if(!strcmp(optarg, "all"))
			{
				begin=0;
				end=0x110000;
			}
			else
			{
				if(!isdigit(optarg[0]))
					temp=-1;
				else
				{
					temp=strtol(optarg, &ptr, 0);
					if(ptr[0]!=',' || !isdigit(ptr[1]))
						temp=-1;
				}
				if(temp<0)
				{
					printf("Not a valid range: %s\n", optarg);
					exit(1);
				}
				else
				{
					begin=temp;
					end=strtol(ptr+1, NULL, 0);
				}
			}
			break;
		case 's':
			size=strtol(optarg, NULL, 0);
			break;
		case 'l':
			cpl=strtol(optarg, NULL, 0);
			break;
		case 'c':
			cell=strtol(optarg, NULL, 0);
			break;
		case 'o':
			out_fn=optarg;
			break;
		case 'a':
			autohinter=1;
			break;
		case 't':
			alpha=1;
			break;
		case 'v':
			++verbose;
			break;
		case 'h':
		case '?':
			usage();
			return 0;
		case 'e':
			seq=1;
			break;
		case 'd':
			def_fn=optarg;
			break;
		case 'p':
			pack=1;
			break;
		}
	}
	if(!strcmp(out_fn, "-"))
		verbose=0;

	if(optind!=argc-1)
	{
		usage();
		return 1;
	}
	
	fn=argv[optind];

	err=FT_Init_FreeType(&freetype);
	if(err)
	{
		fprintf(stderr, "Couldn't initialize FreeType library\n");
		return 1;
	}

	err=FT_New_Face(freetype, fn, 0, &face);
	if(err)
	{
		fprintf(stderr, "Couldn't load font file\n");
		if(err==FT_Err_Unknown_File_Format)
			fprintf(stderr, "Unknown file format\n");
		return 1;
	}

	if(verbose)
	{
		const char *name=FT_Get_Postscript_Name(face);
		printf("Font name: %s\n", name);
		printf("Glyphs:    %ld\n", face->num_glyphs);
	}

	err=FT_Set_Pixel_Sizes(face, 0, size);
	if(err)
	{
		fprintf(stderr, "Couldn't set size\n");
		return 1;
	}

	font.size=size;
	init_font(&font, face, begin, end, autohinter);
	if(pack)
		render_packed(&font);
	else
		render_grid(&font, cell, cpl, seq);
	save_png(out_fn, &font.image, alpha);
	if(def_fn)
		save_defs(def_fn, &font);

	for(i=0; i<font.n_glyphs; ++i)
		free(font.glyphs[i].image.data);
	free(font.glyphs);
	free(font.image.data);

	FT_Done_Face(face);
	FT_Done_FreeType(freetype);

	return 0;
}

unsigned round_to_pot(unsigned n)
{
	n-=1;
	n|=n>>1;
	n|=n>>2;
	n|=n>>4;
	n|=n>>8;
	n|=n>>16;

	return n+1;
}
	
void usage()
{
	printf("ttf2png - True Type Font to PNG converter\n"
		"Copyright (c) 2004-2008  Mikko Rasa, Mikkosoft Productions\n"
		"Distributed under the GNU General Public License\n\n"
		"Usage: ttf2png [options] <TTF file>\n\n"
		"Accepted options (default values in [brackets])\n"
		"  -r  Range of characters to convert in the format low,high [0,255]\n"
		"  -s  Font size to use, in pixels [10]\n"
		"  -l  Number of characters to put in one line [auto]\n"
		"  -c  Character cell size, in pixels [auto]\n"
		"  -o  Output file name (or - for stdout) [font.png]\n"
		"  -a  Force autohinter\n"
		"  -t  Render font to alpha channel\n"
		"  -v  Increase the level of verbosity\n"
		"  -e  Use cells in sequence, rather than by code\n"
		"  -p  Pack the glyphs tightly instead of in a grid\n"
		"  -d  Write a definition to the given file\n"
		"  -h  Print this message\n");
}

void init_font(Font *font, FT_Face face, unsigned first, unsigned last, int autohinter)
{
	unsigned i;
	unsigned size=0;

	font->ascent=(face->size->metrics.ascender+63)>>6;
	font->descent=(face->size->metrics.descender+63)>>6;
	
	if(verbose>=1)
	{
		printf("Ascent:    %d\n", font->ascent);
		printf("Descent:   %d\n", font->descent);
	}

	font->n_glyphs=0;
	font->glyphs=NULL;
	for(i=first; i<=last; ++i)
	{
		unsigned  n;
		FT_Bitmap *bmp=&face->glyph->bitmap;
		int       x, y;
		int       flags=0;
		Glyph     *glyph;

		n=FT_Get_Char_Index(face, i);
		if(!n) continue;

		if(autohinter)
			flags|=FT_LOAD_FORCE_AUTOHINT;
		FT_Load_Glyph(face, n, flags);
		FT_Render_Glyph(face->glyph, FT_RENDER_MODE_NORMAL);

		if(verbose>=2)
			printf("  Char %u: glyph %u, size %dx%d\n", i, n, bmp->width, bmp->rows);

		if(bmp->pixel_mode!=FT_PIXEL_MODE_GRAY)
		{
			fprintf(stderr, "Warning: Glyph %u skipped, not grayscale\n", n);
			continue;
		}

		if(font->n_glyphs>=size)
		{
			size+=16;
			font->glyphs=(Glyph *)realloc(font->glyphs, size*sizeof(Glyph));
		}

		glyph=&font->glyphs[font->n_glyphs++];
		glyph->code=i;
		glyph->image.w=bmp->width;
		glyph->image.h=bmp->rows;
		glyph->image.data=(char *)malloc(bmp->width*bmp->rows);
		glyph->offset_x=face->glyph->bitmap_left;
		glyph->offset_y=face->glyph->bitmap_top-bmp->rows;
		glyph->advance=(int)(face->glyph->advance.x+32)/64;

		if(bmp->pitch<0)
		{
			for(y=0; y<bmp->rows; ++y) for(x=0; x<bmp->width; ++x)
				glyph->image.data[x+(glyph->image.h-1-y)*glyph->image.w]=bmp->buffer[x-y*bmp->pitch];
		}
		else
		{
			for(y=0; y<bmp->rows; ++y) for(x=0; x<bmp->width; ++x)
				glyph->image.data[x+y*glyph->image.w]=bmp->buffer[x+y*bmp->pitch];
		}
	}

	if(verbose>=1)
		printf("Loaded %u glyphs\n", font->n_glyphs);
}

void render_grid(Font *font, unsigned cell, unsigned cpl, int seq)
{
	unsigned i;
	int      top=0, bot=0;
	unsigned first, last;
	unsigned maxw=0, maxh=0;

	for(i=1;; i<<=1)
	{
		first=font->glyphs[0].code&~(i-1);
		last=first+i-1;
		if(last>=font->glyphs[font->n_glyphs-1].code)
			break;
	}

	for(i=0; i<font->n_glyphs; ++i)
	{
		int y;

		y=font->glyphs[i].offset_y+font->glyphs[i].image.h;
		if(y>top)
			top=y;
		if(font->glyphs[i].offset_y<bot)
			bot=font->glyphs[i].offset_y;
		if(font->glyphs[i].image.w>maxw)
			maxw=font->glyphs[i].image.w;
		if(font->glyphs[i].image.h>maxh)
			maxh=font->glyphs[i].image.h;
	}

	if(cell==0)
	{
		cell=top-bot;
		if(maxw>cell)
			cell=maxw;
	}

	if(verbose>=1)
	{
		printf("Max size:  %u x %u\n", maxw, maxh);
		printf("Y range:   [%d %d]\n", bot, top);
		if(maxw>cell || top-bot>cell)
			fprintf(stderr,"Warning: character size exceeds cell size (%d)\n", cell);
	}

	if(cpl==0)
	{
		unsigned count=(seq ? font->n_glyphs : last-first+1);
		for(i=1;; i<<=1)
		{
			cpl=i/cell;
			if(cpl>0 && (count+cpl-1)/cpl<=cpl)
				break;
		}
	}

	font->image.w=round_to_pot(cpl*cell);
	if(seq && font->n_glyphs<last-first+1)
		font->image.h=(font->n_glyphs+cpl-1)/cpl*cell;
	else
		font->image.h=(last-first+cpl)/cpl*cell;
	font->image.h=round_to_pot(font->image.h);
	
	font->image.data=(char *)malloc(font->image.w*font->image.h);
	memset(font->image.data, 255, font->image.w*font->image.h);

	for(i=0; i<font->n_glyphs; ++i)
	{
		Glyph    *glyph;
		int      cx, cy;
		unsigned x, y;

		glyph=&font->glyphs[i];

		if(seq)
		{
			cx=(i%cpl)*cell;
			cy=(i/cpl)*cell;
		}
		else
		{
			cx=((glyph->code-first)%cpl)*cell;
			cy=((glyph->code-first)/cpl)*cell;
		}

		if(cell>glyph->image.w)
			cx+=(cell-glyph->image.w)/2;
		cy+=top-glyph->offset_y-glyph->image.h;

		glyph->x=cx;
		glyph->y=cy;

		for(y=0; y<glyph->image.h; ++y) for(x=0; x<glyph->image.w; ++x)
		{
			if(cx+x<0 || cx+x>=font->image.w || cy+y<0 || cy+y>=font->image.h) continue;
			font->image.data[cx+x+(cy+y)*font->image.w]=255-glyph->image.data[x+y*glyph->image.w];
		}
	}
}

void render_packed(Font *font)
{
	unsigned i;
	unsigned area=0;
	unsigned last_h=0xFFFF;
	char     *used_glyphs;
	char     *used_pixels;
	unsigned cx=0, cy;

	for(i=0; i<font->n_glyphs; ++i)
		area+=(font->glyphs[i].image.w+1)*(font->glyphs[i].image.h+1);

	for(font->image.w=1;; font->image.w<<=1)
	{
		font->image.h=(area*5/4)/font->image.w;
		if(font->image.h<=font->image.w)
			break;
	}
	font->image.h=round_to_pot(font->image.h);
	
	font->image.data=(char *)malloc(font->image.w*font->image.h);
	memset(font->image.data, 255, font->image.w*font->image.h);
	used_pixels=(char *)malloc(font->image.w*font->image.h);
	memset(used_pixels, 0, font->image.w*font->image.h);
	used_glyphs=(char *)malloc(font->n_glyphs);
	memset(used_glyphs, 0, font->n_glyphs);

	for(cy=0; cy<font->image.h;)
	{
		unsigned w;
		unsigned x, y;
		Glyph    *glyph=NULL;
		unsigned best_score=0;
		
		for(; (cx<font->image.w && used_pixels[cx+cy*font->image.w]); ++cx);
		if(cx>=font->image.w)
		{
			cx=0;
			++cy;
			last_h=0xFFFF;
			continue;
		}
		for(w=0; (cx+w<font->image.w && !used_pixels[cx+w+cy*font->image.w]); ++w);

		for(i=0; i<font->n_glyphs; ++i)
		{
			Glyph    *g;

			g=&font->glyphs[i];
			if(!used_glyphs[i] && g->image.w<=w)
			{
				unsigned score;

				score=g->image.h+1;
				if(g->image.h==last_h)
					score*=g->image.w;
				else
					score+=g->image.w;

				if(score>best_score)
				{
					glyph=g;
					best_score=score;
				}
			}
		}

		if(!glyph)
		{
			cx+=w;
			continue;
		}

		used_glyphs[glyph-font->glyphs]=1;
		glyph->x=cx;
		glyph->y=cy;

		for(y=0; y<glyph->image.h; ++y) for(x=0; x<glyph->image.w; ++x)
		{
			if(cx+x<0 || cx+x>=font->image.w || cy+y<0 || cy+y>=font->image.h) continue;
			font->image.data[cx+x+(cy+y)*font->image.w]=255-glyph->image.data[x+y*glyph->image.w];
		}
		for(y=0; y<glyph->image.h+2; ++y) for(x=0; x<glyph->image.w+2; ++x)
		{
			if(cx+x<1 || cx+x>font->image.w || cy+y<1 || cy+y>font->image.h) continue;
			used_pixels[cx+x-1+(cy+y-1)*font->image.w]=1;
		}

		last_h=glyph->image.h;
	}
}

int save_defs(const char *fn, const Font *font)
{
	FILE     *out;
	unsigned i;

	out=fopen(fn, "w");
	if(!out)
	{
		fprintf(stderr, "Couldn't open %s\n",fn);
		return -1;
	}

	fprintf(out, "%d %d %d %d %d\n", font->image.w, font->image.h, font->size, font->ascent, font->descent);
	for(i=0; i<font->n_glyphs; ++i)
	{
		const Glyph *g=&font->glyphs[i];
		fprintf(out, "%u %u %u %u %u %d %d %d\n", g->code, g->x, g->y, g->image.w, g->image.h, g->offset_x, g->offset_y, g->advance);
	}

	fclose(out);

	return 0;
}

int save_png(const char *fn, const Image *image, char alpha)
{
	FILE       *out;
	png_struct *pngs;
	png_info   *pngi;
	png_byte   *rows[image->h];
	int        i;
	png_byte   *data2;
	int        color;

	if(!strcmp(fn, "-"))
		out=stdout;
	else
	{
		out=fopen(fn, "wb");
		if(!out)
		{
			fprintf(stderr, "Couldn't open %s\n",fn);
			return -1;
		}
	}

	pngs=png_create_write_struct(PNG_LIBPNG_VER_STRING, NULL, NULL, NULL);
	if(!pngs)
	{
		fprintf(stderr, "Error writing PNG file\n");
		return -1;
	}
	pngi=png_create_info_struct(pngs);
	if(!pngi)
	{
		png_destroy_write_struct(&pngs, NULL);
		fprintf(stderr, "Error writing PNG file\n");
		return -1;
	}

	png_init_io(pngs, out);
	if(alpha)
	{
		data2=(png_byte *)malloc(image->w*image->h*2);
		for(i=0; i<image->w*image->h; ++i)
		{
			data2[i*2]=255;
			data2[i*2+1]=255-image->data[i];
		}
		for(i=0; i<image->h; ++i)
			rows[i]=(png_byte *)(data2+i*image->w*2);
		color=PNG_COLOR_TYPE_GRAY_ALPHA;
	}
	else
	{
		for(i=0; i<image->h; ++i)
			rows[i]=(png_byte *)(image->data+i*image->w);
		color=PNG_COLOR_TYPE_GRAY;
	}
	png_set_IHDR(pngs, pngi, image->w, image->h, 8, color, PNG_INTERLACE_NONE, PNG_COMPRESSION_TYPE_DEFAULT, PNG_FILTER_TYPE_DEFAULT);
	png_set_rows(pngs, pngi, rows);
	png_write_png(pngs, pngi, PNG_TRANSFORM_IDENTITY, NULL);
	png_destroy_write_struct(&pngs, &pngi);
	if(alpha)
		free(data2);

	if(verbose) printf("Saved %dx%d PNG image to %s\n", image->w, image->h, fn);

	fclose(out);

	return 0;
}
