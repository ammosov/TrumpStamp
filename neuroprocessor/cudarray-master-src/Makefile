

SRC_DIR = ./src

SRCS = $(SRC_DIR)/nnet/conv_bc01_matmul.cpp \
       $(SRC_DIR)/nnet/pool_b01.cpp \
       $(SRC_DIR)/nnet/cudnn.cpp

CUDA_SRCS = $(SRC_DIR)/array_ops.cu \
            $(SRC_DIR)/elementwise.cu \
            $(SRC_DIR)/reduction.cu \
            $(SRC_DIR)/blas.cu \
            $(SRC_DIR)/random.cu \
            $(SRC_DIR)/image/img2win.cu \
            $(SRC_DIR)/image/rescale.cu \
            $(SRC_DIR)/nnet/one_hot.cu


INCLUDE_DIRS = ./include
INCLUDE_DIRS += $(CUDA_PREFIX)/include


LIB_DIRS += $(CUDA_PREFIX)/lib
LIBS += cudart cublas cufft curand

C_FLAGS += -DCUDNN_ENABLED
LIBS += cudnn



CUDA_ARCH = -gencode arch=compute_20,code=sm_20 \
              -gencode arch=compute_20,code=compute_20 \
              -gencode arch=compute_30,code=sm_30 \
              -gencode arch=compute_30,code=compute_30 \
              -gencode arch=compute_35,code=sm_35 \
              -gencode arch=compute_35,code=compute_35


export PATH := $(CUDA_PREFIX)/bin:$(PATH)

CXX = cl.exe
NVCC = nvcc
BUILD_DIR = ./build
OBJS = $(SRCS:.cpp=.o) $(CUDA_SRCS:.cu=.o)
LIBCUDARRAY = libcudarray.lib
LIBCUDARRAY_BUILD = $(BUILD_DIR)/$(LIBCUDARRAY)
LIBCUDARRAY_INSTALL = $(INSTALL_PREFIX)/lib/$(LIBCUDARRAY)

INCLUDES += $(foreach include_dir,$(INCLUDE_DIRS),-I$(include_dir))
C_FLAGS += -D_FORCE_INLINES
NVCC_FLAGS = $(CUDA_ARCH) -O3 --compiler-options '$(C_FLAGS)' \
             --ftz=true --prec-div=false -prec-sqrt=false --fmad=true
LDFLAGS += $(foreach lib_dir,$(LIB_DIRS),-L$(lib_dir)) \
	       $(foreach lib,$(LIBS),-l$(lib))


$(LIBCUDARRAY_BUILD) : $(OBJS)
	mkdir -p $(BUILD_DIR)
	$(CXX) -shared $(C_FLAGS) -o $@ $^ $(LDFLAGS)

%.o : %.cpp
	$(CXX) $(C_FLAGS) $(INCLUDES) -c -o $@ $<

%.o : %.cu
	$(NVCC) $(NVCC_FLAGS) $(INCLUDES) -c -o $@ $<

all: $(LIBCUDARRAY_BUILD)

$(LIBCUDARRAY_INSTALL) : $(LIBCUDARRAY_BUILD)
	cp $(LIBCUDARRAY_BUILD) $(LIBCUDARRAY_INSTALL)

install: $(INSTALL_PREFIX)/lib/$(LIBCUDARRAY)

uninstall:
	rm $(LIBCUDARRAY_INSTALL)

.PHONY: clean
clean:
	rm -f $(OBJS) $(LIBCUDARRAY_BUILD)
