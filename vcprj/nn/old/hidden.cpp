// #include "hidden.h"
// #include "layout.h"
// #include "neuron.h"
// #include "connect.h"

// HiddenLayout::HiddenLayout()
// {
//     size_t neuronIdx = 0;
//     size_t depthIdx = 0;

//     for (auto layout : layouts) {
//         for (auto neuron : layout) {
//             neuron = new Neuron(NeuronType::HIDDEN, neuronIdx++, "_LEVEL_" +
//             to_string(depthIdx++));
//         }
//     }

//     // for (auto n = 0; n < size; n++) {
//     //     neurons.push_back(new Neuron(_type, idx++, level));
//     // }

//     // for (auto d = 0; d < depth; d++) {
//     //     auto layout = new Layout(size, NeuronType::HIDDEN, "_LEVEL_" + to_string(d));

//     //     layouts.push_back(layout);

//     //     if (d > 0) {
//     //         layouts[d - 1]->bind(layout);
//     //     }
//     // }
// }

// HiddenLayout::~HiddenLayout() {}

// void HiddenLayout::learning()
// {
//     for (auto layout : layouts) {
//         layout->learning();
//     }
// }

// void HiddenLayout::calcDelta()
// {
//     calc();

//     for (auto layout : layouts) {
//         for (auto neuron : layout->neurons) {
//             float delta = .0f;

//             for (auto neuronBack : neuron->backs) {
//                 float weight = .0f;

//                 for (auto connect : neuronBack->connects) {
//                     if (connect->way == neuron) {
//                         weight = connect->weight;
//                         break;
//                     }
//                 }

//                 delta += neuronBack->delta * weight;
//             }

//             neuron->delta = ((1 - neuron->power) * neuron->power) * delta;
//         }
//     }
// }

// void HiddenLayout::calc()
// {
//     for (auto layout : layouts) {
//         layout->process();
//     }
// }
