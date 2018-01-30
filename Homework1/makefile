CXX = g++
CXXFLAGS = -Wall -pedantic -std=c++11 -g3

Kayles.16: main.o
	${CXX} ${CXXFLAGS} -o Kayles.16 main.o

main.o: main.cpp
	${CXX} ${CXXFLAGS} -c main.cpp

clean:
	rm -rf main.o Kayles.16 	
