CXX = g++
CXXFLAGS = -Wall -pedantic -std=c++11 -g3

Pig: pig.o
	${CXX} ${CXXFLAGS} -o Pig pig.o

pig.o: pig.cpp
	${CXX} ${CXXFLAGS} -c pig.cpp

clean:
	rm -rf pig.o Pig

