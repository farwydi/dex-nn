#!/bin/sh

g++ -c -o tmp/connect.o nn/connect.cpp
g++ -c -o tmp/neuron.o nn/neuron.cpp
g++ -c -o tmp/nn.o nn/nn.cpp
g++ -c -o tmp/test.o nn/test.cpp

g++ -o nn.exe tmp/connect.o tmp/neuron.o tmp/nn.o tmp/test.o
