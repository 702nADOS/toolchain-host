#TARGET += is the name of the binary to be created. This is the only mandatory variable to be defined in a target.mk file.
TARGET = cond_42

#REQUIRES += expresses the requirements that must be satisfied in order to build the target. You find more details about the underlying mechanism in Section Specializations.

#LIBS += is the list of libraries that are used by the target.
#LIBS = base libc stdcxx
LIBS = base

#SRC_CC += contains the list of .cc source files. The default search location for source codes is the directory, where the target.mk file resides.
SRC_CC = cond_42.cpp

#SRC_C += contains the list of .c source files.

#SRC_S += contains the list of assembly .s source files.

#SRC_BIN += contains binary data files to be linked to the target.

#INC_DIR += is the list of include search locations. Directories should always be appended by using +=. Never use an assignment!

#EXT_OBJECTS += is a list of Genode-external objects or libraries. This variable is mostly used for interfacing Genode with legacy software components.

#Rarely used variables
#CC_OPT += contains additional compiler options to be used for .c as well as for .cc files.

#CC_CXX_OPT += contains additional compiler options to be used for the C++ compiler only.

#CC_C_OPT += contains additional compiler options to be used for the C compiler only.
