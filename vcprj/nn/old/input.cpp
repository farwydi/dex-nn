// #include "input.h"
// #include "layout.h"
// #include "hidden.h"
// #include "neuron.h"

// InputLayout::InputLayout(unsigned short _size, HiddenLayout *hidden)
// 	: size(_size)
// {
// 	if (size > 0) {
// 		layout = new Layout(size, NeuronType::INPUT);

// 		hidden->layouts[0]->bind(layout);
// 	}
// }

// InputLayout::~InputLayout()
// {
// }

// void InputLayout::set(unsigned short number, float value)
// {
// 	if (number > size) {
// 		return; // error
// 	}

// 	layout->neurons[number]->power = value;
// }

// void InputLayout::learning(float E, float A)
// {
// 	layout->learning(E, A);
// }
