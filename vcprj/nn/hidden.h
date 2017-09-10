#pragma once

#include "precompilation.h"

class HiddenLayout
{
public:
	HiddenLayout(unsigned short _size = 10, unsigned short _depth = 2);
	~HiddenLayout();

	void learning(float E, float A);

	void calcDelta();

	void calc();

	unsigned short size;
	unsigned short depth;

	vector<Layout*> layouts;
};