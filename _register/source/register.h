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
