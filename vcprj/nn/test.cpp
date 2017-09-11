#include "nn.h"

#include <iostream>

#undef LEARNING_TIME
#define LEARNING_TIME .15f

#undef FORCE_ALPHA
#define FORCE_ALPHA .3f

#undef INPUT_SIZE
#define INPUT_SIZE 2

#undef HIDDEN_DEPTH
#define HIDDEN_DEPTH 1

#undef HIDDEN_SIZE
#define HIDDEN_SIZE 3

#undef OUTPUT_SIZE
#define OUTPUT_SIZE 1

int main()
{
    auto _nn = new NeuralNetwork();

    array<array<NN_POINT, INPUT_SIZE + 1>, 4> _test;
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

    // leaning
    array<NN_POINT, INPUT_SIZE> sets;
    array<NN_POINT, OUTPUT_SIZE> corrects;

    for (auto epoch = 0; epoch < 80000; epoch++) {
        for (auto params : _test) {
            sets[0] = params[0];
            sets[1] = params[1];
            _nn->set(sets);

            corrects[0] = params[2];
            auto mse = _nn->mse(_nn->learning(corrects), corrects);
            auto _mse = mse[0] * 100.f;

            cout << "Error: " + to_string(_mse) << endl;
        }
    }

    return 0;
}
