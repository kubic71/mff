using OpenTK;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace _086shader
{
  public class CatmullRom
  {
    double[] Points;
    public float TimeLength => Points.Length - 3;

    public CatmullRom (double[] points)
    {
      Points = points;
    }

    public CatmullRom (float[] points)
    {
      Points = new double[points.Length];

      for (int i = 0; i < points.Length; i++)
      {
        Points[i] = points[i];
      }
    }


    public double GetVal (double time)
    {
      if (time < 0 || time >= Points.Length - 3)
      {
        throw new ArgumentException($"time must be between {0} and {Points.Length - 3}");
      }

      time += 1;

      int n = (int)Math.Floor(time);
      double t = time - n;


      double p0 = Points[n-1];
      double p1 = Points[n];
      double p2 = Points[n+1];
      double p3 = Points[n+2];
      return 0.5 * (Math.Pow(t, 3) * (-p0 + 3 * p1 - 3 * p2 + p3) +
                    Math.Pow(t, 2) * (2 * p0 - 5 * p1 + 4 * p2 - p3) +
                    t * (-p0 + p2) +
                    2 * p1);
    }
  }


  public class SquadInterpolator
  {

    // Inspired mainly by:
    // https://web.mit.edu/2.998/www/QuaternionReport1.pdf

    // Took many many many hours to debug and get working :D 

    Quaternion[] keyFrames { get; set; }

    private Quaternion Conjugate (Quaternion q)
    {
      if (Math.Abs(q.Length - 1) > 0.000001)
      {
        throw new ArgumentException("Sanity check, unit quaternion expected");
      }

      var ret = new Quaternion();
      ret.W = q.W;
      ret.Xyz = -q.Xyz;
      return ret;

    }

    private Quaternion q (int i) => keyFrames[i];
    private Quaternion s (int i)
    {
      return q(i) * Exp(-0.25f * (Log(Conjugate(q(i)) * q(i + 1)) + Log(Conjugate(q(i)) * q(i - 1))));
    }

    private Quaternion Log (Quaternion q)
    {
      // q must be unit quaternion!
      if (Math.Abs(q.Length - 1) > 0.000001)
        throw new ArgumentException("Log can handle only unit quaternions, |q| = " + q.Length);

      if (q.Xyz.Length < 0.000001)
      {
        return new Quaternion(0, 0, 0, 0);
      }


      // Let q = [cos(theta), sin(theta) * v], |v| = 1
      var v = q.Xyz.Normalized();
      var sin = q.Xyz.Length;
      var cos = q.W;
      var theta = (float)Math.Atan2(sin, cos);

      var res = new Quaternion();
      // log [cos(theta), sin(theta) * v ] = [0, theta * v ]
      res.W = 0;
      res.Xyz = theta * v;

      return res;
    }

    private Quaternion Exp (Quaternion q)
    {
      // Let q = w + xi + yj + zk
      // Let v = (x, y, ,z)  3d vector
      // then q can be written as q = [w, v] 
      // 
      // assume q = [0, theta * v], |v| = 1
      // exp(q) = [cos(theta), sin(theta) * v]

      // sanity check
      if (Math.Abs(q.W) > 0.000001)
        throw new ArgumentException("Can do exponentials only of pure vectors");

      // q = [0, u] = [0, theta * v], |v| = 1
      // therefore |u| = theta * |v| = theta
      // v = u / theta
      // note that there are 2 solutions, the second is -v, -theta
      float theta = (float)Math.Sqrt(q.X*q.X + q.Y*q.Y + q.Z*q.Z);
      if (theta < 0.000001)
      {
        return new Quaternion(0, 0, 0, 1);
      }

      var sin = (float)Math.Sin(theta);
      Quaternion res = new Quaternion();

      // v = u / theta
      var v = (new Vector3(q.X, q.Y, q.Z)) / theta;

      // exp(q) = [cos(theta), sin(theta) * v]
      res.Xyz = sin * v;
      res.W = (float)Math.Cos(theta);
      return res;
    }

    public SquadInterpolator (Quaternion[] frames)
    {

      // Squad requiers one additional control quaternion at each end of a sequence
      List<Quaternion> keyFrameList = new List<Quaternion>();

      // starting control point is the same as first point
      keyFrameList.Add(frames[0]);
      foreach (var frame in frames)
        keyFrameList.Add(frame);

      keyFrameList.Add(frames[frames.Length - 1]);
      keyFrames = keyFrameList.ToArray();

      // q and -q unit quaternions represent the same rotation ( 90deg rotation around x-axis can be represented by 270deg rotation around -x-axis )
      // but Quaternion.Slerp(q1, q2, t) automatically flips q2 in case q1 and (-q2) are closer (angle-wise) than q1 and q2.
      // tangent computation doesn't take the flip into account and expetcs the Slerp to be interpolating original q1 and q2, which causes glitches
      // to avoid that, we need to make sure, that neighbouring quaternions form an acute angle

      for (int i = 0; i < keyFrames.Length - 1; i++)
      {
        var cosAngle = DotProduct(keyFrames[i], keyFrames[i+1]);
        if (cosAngle < 0)
        {
          keyFrames[i + 1] *= -1;
        }
        else if (cosAngle == 0)
        {
          // quaternions are perpendicular, which means SLERP is undefined
          // throw new ArgumentException("cannot interpolate between perpendicular quaternions");
        }
      }
    }

    private float DotProduct (Quaternion q1, Quaternion q2)
    {
      return q1.X * q2.X + q1.Y * q2.Y + q1.Z * q2.Z + q1.W * q2.W;
    }

    public Quaternion GetVal (float time)
    {
      if (time < 0 || time >= keyFrames.Length - 3)
      {
        throw new ArgumentException($"time must be between {0} and {keyFrames.Length - 3}");
      }

      time += 1;
      int i = (int)Math.Floor(time);
      float h = time - i;
      return Squad(i, h);
    }



    private Quaternion Slerp (Quaternion q1, Quaternion q2, float t)
    {
      // Only unit quaternions are valid rotations.
      // Normalize to avoid undefined behavior.
      if (Math.Abs(q1.Length - 1) > 0.001 || Math.Abs(q1.Length - 1) > 0.001)
      {
        throw new ArgumentException("Quaternion is not normalized in slerp!");
      }

      // Compute the cosine of the angle between the two vectors.
      float dot = DotProduct(q1, q2);

      // If the dot product is negative, slerp won't take
      // the shorter path. Quaternion.Slerp in that case flips one quaternion, so that shorter path is taken.
      // But this behaviour is undesirable in squad.
      // therefore we need to implement our own Slerp

      const float DOT_THRESHOLD = 0.9995f;
      if (dot > DOT_THRESHOLD)
      {
        // If the inputs are too close for comfort, linearly interpolate
        // and normalize the result.
        Quaternion result = q1 + t*(q2 - q1);
        result.Normalize();
        return result;
      }

      var theta_0 = Math.Acos(dot);        // theta_0 = angle between input vectors
      var theta = theta_0*t;          // theta = angle between v0 and result
      var sin_theta = Math.Sin(theta);     
      var sin_theta_0 = Math.Sin(theta_0); 

      float s1 = (float)(Math.Cos(theta) - dot * sin_theta / sin_theta_0);  // == sin(theta_0 - theta) / sin(theta_0)
      float s2 = (float)(sin_theta / sin_theta_0);

      return (s1 * q1) + (s2 * q2);
    }

    private bool Obtuse (Quaternion q1, Quaternion q2)
    { // return true when q1 and q2 form an obtuse angle
      if (DotProduct(q1, q2) < 0)
      {
        return true;
      }
      return false;
    }

    private Quaternion Squad (int i, float h)
    {
      return Slerp(Slerp(q(i), q(i + 1), h), Slerp(s(i), s(i + 1), h), 2 * h * (1 - h));
    }
  }

  public class TrajectoryInterpolator
  {
    CatmullRom cx;
    CatmullRom cy;
    CatmullRom cz;
    public float TimeLength => cx.TimeLength;
    public TrajectoryInterpolator (Vector3[] points)
    {
      // CatmullRom requiers one additional point at each end of a sequence
      List<Vector3> cm_points = new List<Vector3>();

      // starting control point is the same as first point
      cm_points.Add(new Vector3(points[0]));
      foreach (var p in points)
        cm_points.Add(p);
      cm_points.Add(new Vector3(points[points.Length - 1]));

      points = cm_points.ToArray();
      cx = new CatmullRom(GetDimCoords(points, 0));
      cy = new CatmullRom(GetDimCoords(points, 1));
      cz = new CatmullRom(GetDimCoords(points, 2));

    }

    private float[] GetDimCoords (Vector3[] points, int dim)
    {
      float[] coords = new float[points.Length];
      for (int i = 0; i < points.Length; i++)
      {
        switch (dim)
        {
          case 0:
            coords[i] = points[i].X;
            break;
          case 1:
            coords[i] = points[i].Y;
            break;
          case 2:
            coords[i] = points[i].Z;
            break;
          default:
            throw new ArgumentException();
        }
      }

      return coords;
    }

    public Vector3 GetVec (double time)
    {
      return new Vector3((float)cx.GetVal(time), (float)cy.GetVal(time), (float)cz.GetVal(time));
    }
  }
}
