#include "connect.h"
#include "nn.h"

#include <iostream>

void main()
{
	//# init
	auto _nn = new NeuralNetwork(2, 1, 3, 1);

	array<array<float, 3>, 4 > _test;
	_test[0][0] = .0f;
	_test[0][1] = .0f;
	_test[0][2] = .0f;

	_test[1][0] = .0f;
	_test[1][1] = 1.f;
	_test[1][2] = 1.f;

	_test[2][0] = 1.f;
	_test[2][1] = .0f;
	_test[2][2] = 1.f;

	_test[3][0] = 1.f;
	_test[3][1] = 1.f;
	_test[3][2] = .0f;

	_nn->setEA(.15f, .3f);

	//# leaning
	float *sets = new float[2];
	float *corrects = new float[1];

	for (auto epoch = 0; epoch < 80000; epoch++) {
		for (auto params : _test) {

			sets[0] = params[0];
			sets[1] = params[1];
			_nn->set(sets, 2);

			corrects[0] = params[2];
			_nn->learning(corrects, 1);

			auto rr = _nn->result();
			auto mse = _nn->mse(rr, 1, corrects, 1);
			auto _mse = mse[0] * 100.f;
			delete mse;
			delete rr;

			cout << "Error: " + to_string(_mse) << endl;
		}
	}

	system("PAUSE");
}