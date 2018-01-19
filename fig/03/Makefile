
all : plots

plots : amdahls_law.svg

amdahls_law.svg : amdahls_law.R
	@./amdahls_law.R

amdahls_law.png : amdahls_law.R
	@./amdahls_law.R

clean :
	@rm -fv *svg *png
