#include <stdio.h>
#include <math.h>
#include <stdlib.h>

/*
Analytic functions to compute eclipse and transit light-curve shapes.
Based on code from Photometry for Orbits, Eclipses, and Transits.
Equations based on Mandel & Agol 2002.
*/

double mandeltr(double t,
		double tc,
		double rprs,
		double i,
		double ars,
		double p,
		double flux);
double mandeltr(double t,    // time of flux calc
		double tc,   // time of transit
		double rprs, // planet radius as fraction of stellar radius
		double i,    // inclination (radians)
		double ars,  // semimajor axis as fraction of stellar radius
		double p,    // orbital period
		double flux) // system flux
{
  double z, mod, k0, k1;
  double y = 1;
  double PI = 3.141592653589793;
  mod = (t - tc) - floor((t - tc)/p)*p;
  if((mod > p/4.) && (mod < 3*p/4.))
    {
      z = ars;
    }
  else
    {
      z = ars*sqrt(pow(sin(2*PI*(tc-t)/p),2)+\
		   pow((cos(i)*cos(2*PI*(tc-t)/p)),2));
    }
  if(z<=(1-rprs))
    {
      y = 1-pow(rprs,2);
    }
  if(z>(1-rprs)&&z<=(1+rprs))
    {
      k0 = acos((rprs*rprs+z*z-1)/2/rprs/z);
      k1 = acos((1-rprs*rprs+z*z)/2/z);
      y  = 1-1/PI*(k0*rprs*rprs+k1-sqrt((4*z*z-\
				   pow((1+z*z-rprs*rprs),2))/4));
    }

  y *= flux;

  return y;
}

double mandelecl(double t,
		 double te,
		 double frat,
		 double i,
		 double ars,
		 double p,
		 double rprs,
		 double flux);
double mandelecl(double t,    // time of flux calc
		 double te,   // time of eclipse
		 double frat, // planet-to-star flux ratio
		 double i,    // inclination (radians)
		 double ars,  // semimajor axis as fraction of stellar radius
		 double p,    // orbital period
		 double rprs, // planet-to-star radius ratio
		 double flux) // system flux
{
  double z, mod, k0, k1;
  double y = 1;
  double PI = 3.141592653589793;
  // Save computation time if eclipse depth is 0
  if(frat == 0)
    {
      y *= flux;
      return y;
    }
   
  mod = (t - te) - floor((t - te)/p)*p;
  if((mod > p/4.) && (mod < 3*p/4.))
    {
      z = ars;
    }
  else
    {
      z = ars*sqrt(pow(sin(2*PI*(te-t)/p),2)+\
		   pow((cos(i)*cos(2*PI*(te-t)/p)),2));
    }
  if(z<=(1-rprs))
    {
      y = 1-frat;
    }
  if(z>(1-rprs)&&z<=(1+rprs))
    {
      k0 = acos((rprs*rprs+z*z-1)/2/rprs/z);
      k1 = acos((1-rprs*rprs+z*z)/2/z);
      y  = 1/PI*(k0*rprs*rprs+k1-sqrt((4*z*z-\
				 pow((1+z*z-rprs*rprs),2))/4));
      y  = 1-frat/rprs/rprs*y;
    }

  y *= flux;
  return y;
}
