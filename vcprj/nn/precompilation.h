#pragma once

#include <array>
#include <cmath>
#include <map>
#include <string>
#include <cstring>
#include <vector>
#include <fstream>

class Connect;
class Neuron;
class Layout;
class HiddenLayout;
class InputLayout;
class ResultLayout;
class NeuralNetwork;

enum NeuronType
{
    INPUT,
    OUTPUT,
    HIDDEN
};

#define USE_LIMITER_CONNECTER 0

#if USE_LIMITER_CONNECTER == 1
const int COUNT_CONNECTS = 3;
#endif // USE_LIMITER_CONNECTER == 1

const int HIDDEN_DEPTH = 1;
const int HIDDEN_SIZE = 48;

const int INPUT_SIZE = 32;
const int OUTPUT_SIZE = 28;

#define NN_POINT float

const NN_POINT LEARNING_TIME = .15f;
const NN_POINT FORCE_ALPHA = .3f;

// #define USE_NORMALIZE_FUNC 0

using namespace std;
