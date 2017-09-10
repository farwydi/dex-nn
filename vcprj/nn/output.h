#pragma once

#include "precompilation.h"

class ResultLayout
{
public:
	ResultLayout(unsigned short _size, HiddenLayout *_hidden);
	~ResultLayout();

	float* result();

	void learning(float *correct, size_t correctSize, float E, float A);

	unsigned short size;

	HiddenLayout *hidden;
	Layout *layout;
};