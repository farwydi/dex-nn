#pragma once

#include "precompilation.h"

class InputLayout
{
public:
	InputLayout(unsigned short _size, HiddenLayout *hidden);
	~InputLayout();

	void set(unsigned short number, float value);

	void learning(float E, float A);

	unsigned short size;

	Layout *layout;
};