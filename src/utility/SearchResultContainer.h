#pragma once
#include "ResultContainer.h"
#include <iostream>

using namespace std;

struct SearchResultContainer : ResultContainer
{
    double initialH;
    string soltuionPath;
};
