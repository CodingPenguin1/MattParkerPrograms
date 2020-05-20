// typedef struct {
//     unsigned long long int lo;
//     unsigned long long int hi;
//   } my_uint128;

//   my_uint128 add_uint128 (my_uint128 a, my_uint128 b)
//   {
//     my_uint128 res;
//     res.lo = a.lo + b.lo;
//     res.hi = a.hi + b.hi + (res.lo < a.lo);
//     return res;
//   }

// https://github.com/curtisseizert/CUDA-uint128
#include <stdint.h>
#include <iostream>

#define SLOTS_PER_BLOCK 1024

#define NUM_THREADS 256
#define NUM_BLOCKS 256

__constant__ uint64_t POWS[19] = {1ll, 10ll, 100ll, 1000ll, 10000ll, 100000ll, 1000000ll,
                                  10000000ll, 100000000ll, 1000000000ll, 10000000000ll,
                                  100000000000ll, 1000000000000ll, 10000000000000ll,
                                  100000000000000ll, 1000000000000000ll, 10000000000000000ll,
                                  100000000000000000ll, 1000000000000000000ll};


__global__ void isPolydivisible(uint64_t maxNum, uint64_t *results) {

    uint64_t start = blockIdx.x * blockDim.x + threadIdx.x;
    uint64_t stride = blockDim.x * gridDim.x;

    uint16_t numberFound = 0;
    uint64_t *threadResults = results + start * SLOTS_PER_BLOCK;

    for(uint64_t n = start; n < maxNum; n += stride) {
        bool polydivisible = true;
        uint16_t numDigits = 1;

        for(int i = 0; i < 19; ++i) {
            if(n >= POWS[i]) {
                numDigits = i + 1;
            }
        }

        __syncthreads();

        for(int i = 0; i < numDigits; ++i) {
            uint64_t num = n / POWS[i];
            if (num % (numDigits - i) != 0)
                polydivisible = false;
        }

        if(polydivisible)
            threadResults[numberFound++] = n;

        // Maybe sync threads?
    }
}


int main() {

    std::cout << "Enter the maximum number: " << std::flush;
    uint64_t maxNum = 0;
    std::cin >> maxNum;

    uint64_t *results;
    uint64_t arrLen = SLOTS_PER_BLOCK * NUM_BLOCKS * NUM_THREADS;
    cudaMallocManaged(&results, arrLen  * sizeof(uint64_t) );

    for(uint64_t i = 0; i < arrLen; ++i) {
        results[i] = 0;
    }

    cudaEvent_t start, stop;

    cudaEventCreate(&start);
    cudaEventCreate(&stop);

    cudaEventRecord(start);

    isPolydivisible<<<NUM_BLOCKS,NUM_THREADS>>>(maxNum, results);

    cudaEventRecord(stop);
    cudaEventSynchronize(stop);

    float millis = 0;
    cudaEventElapsedTime(&millis, start, stop);

    uint64_t count = 1;
    for(uint64_t i = 0; i < arrLen; ++i) {
        if(results[i] != 0) {
            std::cout << results[i] << "\n";
            ++count;
        }
    }

    std::cout << std::flush;

    printf("%0.3fs, %d numbers found\n", millis / 1000, count);
}
