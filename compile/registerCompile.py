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

ffibuilder.set_source("_register",  # name of the output C extension
"""
    #include "../_register/source/register.h"',
""",
    sources=['../_register/source/register.c'],   # includes pi.c as additional sources
    libraries=[])    # on Unix, link with the math library

if __name__ == "__main__":
    ffibuilder.compile(tmpdir="../_register/", verbose=True)