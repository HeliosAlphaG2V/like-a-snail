from os import getcwd, path
from cffi import FFI
ffibuilder = FFI()

ffibuilder.cdef("""
struct reg {
  int A;
  int B;
  int C;
  int D;
  int E;
  int H;
  int L;
  unsigned short PC;
  unsigned short SP;
} registerC;
struct regF {
  unsigned char Z:1;
  unsigned char N:1;
  unsigned char H:1;
  unsigned char C:1;
} registerFlags;
int getAF();
int getBC();
int getDE();
int getHL();
void setAF(int r16);
void setBC(int r16);
void setDE(int r16);
void setHL(int r16);
""")

person_header = """
#ifndef REGISTER_H_
#define REGISTER_H_

struct reg {
  int A;
  //  F = regF
  int B;
  int C;
  int D;
  int E;
  int H;
  int L;
  unsigned short PC;
  unsigned short SP;
} registerC;

struct regF {
  unsigned char Z:1;
  unsigned char N:1;
  unsigned char H:1;
  unsigned char C:1;
} registerFlags;

int getAF();
int getBC();
int getDE();
int getHL();
void setAF(int r16);
void setBC(int r16);
void setDE(int r16);
void setHL(int r16);

#endif

"""

#path.join(path.normpath(path.join(getcwd())), 'register\\source\\register.c')
ffibuilder.set_source("lasregister",  # name of the output C extension
                      person_header,
                      sources=[path.join(path.normpath(path.join(getcwd())), path.normpath('lasregister/source/register.c'))],
                      libraries=[])

if __name__ == "__main__":
    ffibuilder.compile(tmpdir='lasregister/tmp', verbose=True, target='lasregister.*')
