#include "register.h"

int getAF() {
	return (registerC.A << 8) |
		   (registerFlags.Z << 7) |
		   (registerFlags.N << 6) |
		   (registerFlags.H << 5) |
		   (registerFlags.C << 4);

	// 0, 1 , 2, 3 are locked
}

int getBC() {
	return (registerC.B << 8) | registerC.C;
}

int getDE() {
	return (registerC.D << 8) | registerC.E;
}

int getHL() {
	return (registerC.H << 8) | registerC.L;
}

void setHL(int r16) {
	registerC.H = (r16 & 0xFF00) >> 8;
	registerC.L = r16 & 0x00FF;
}
void setAF(int r16) {
	registerC.A = (r16 & 0xFF00) >> 8;
	registerFlags.Z = (r16 & 0x0080) >> 7;
	registerFlags.N = (r16 & 0x0040) >> 6;
	registerFlags.H = (r16 & 0x0020) >> 5;
	registerFlags.C = (r16 & 0x0010) >> 4;
}
void setBC(int r16) {
	registerC.B = (r16 & 0xFF00) >> 8;
	registerC.C = r16 & 0x00FF;
}
void setDE(int r16) {
	registerC.D = (r16 & 0xFF00) >> 8;
	registerC.E = r16 & 0x00FF;
}
