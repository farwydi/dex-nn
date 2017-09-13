//#include "nn.h"
//#include "connect.h"
//#include "neuron.h"
//
//#include <iostream>
//
//#undef INPUT_SIZE
//#define INPUT_SIZE 2
//
//#undef HIDDEN_DEPTH
//#define HIDDEN_DEPTH 1
//
//#undef HIDDEN_SIZE
//#define HIDDEN_SIZE 2
//
//#undef OUTPUT_SIZE
//#define OUTPUT_SIZE 1
//
//int mai1n()
//{
//    auto __nn = new NeuralNetwork();
//
//    array<NN_POINT, INPUT_SIZE> sets;
//    sets[0] = 1.f;
//    sets[1] = .0f;
//    __nn->set(sets);
//
//    // h1 w1
//    __nn->hidden[0][0]->connects[0]->weight = 0.45f;
//    // h1 w3
//    __nn->hidden[0][0]->connects[1]->weight = -0.12f;
//    // h2 w2
//    __nn->hidden[0][1]->connects[0]->weight = 0.78f;
//    // h2 w4
//    __nn->hidden[0][1]->connects[1]->weight = 0.13f;
//
//    __nn->output[0]->connects[0]->weight = 1.5f;
//    __nn->output[0]->connects[1]->weight = -2.3f;
//
//
//    __nn->result();
//    if (abs(__nn->output[0]->power - 0.34f) < 0.0001f) {
//        cout << "ERROR" << endl;
//    }
//
//    array<NN_POINT, OUTPUT_SIZE> corrects;
//    corrects[0] = 1.f;
//    __nn->learning(corrects);
//    if (abs(__nn->output[0]->power - 0.37f) < 0.0001f) {
//        cout << "ERROR" << endl;
//    }
//
//    cout << "TEST done" << endl;
//
//    return 0;
//}
