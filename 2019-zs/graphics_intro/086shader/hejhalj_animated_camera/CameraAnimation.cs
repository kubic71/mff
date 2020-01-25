using OpenTK;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace _086shader
{
  public abstract class CameraAnimation
  {
    public float MaxTime { get; protected set; }
    protected TrajectoryInterpolator positionInterpolator;

    public virtual Vector3 GetPosition (float time)
    {
      return positionInterpolator.GetVec(time);
    }

    public abstract Matrix4 GetModelViewMatrix(float time);
  }


  public class CameraManual : CameraAnimation
  {
    SquadInterpolator orientationInterpolator; 
    Vector3[] positions;

    public CameraManual(Vector3[] positions, Vector3[] lookAts, Vector3[] lookUps)
    {
      MaxTime = positions.Length - 1;
      this.positions = positions;


      // create squad interpolator
      var orientations = new Quaternion[lookAts.Length];

      for (int i = 0; i < orientations.Length; i++)
      {
        orientations[i] = ToQuaternion(positions[i], lookAts[i], lookUps[i]);
      }
      orientationInterpolator = new SquadInterpolator(orientations);
      positionInterpolator = new TrajectoryInterpolator(positions);
    }

    public override Matrix4 GetModelViewMatrix (float time)
    {
      var camera = Matrix3.CreateFromQuaternion(orientationInterpolator.GetVal(time));
      camera.Transpose();

      var position = GetPosition(time);

      // camera.Row2 - forward vector
      // camera.Row1 - up vector
      return Matrix4.LookAt(position, position + camera.Row2, camera.Row1);
    }

    public Quaternion ToQuaternion(Vector3 Position, Vector3 LookAt, Vector3 Up)
    {
      Up = Vector3.Normalize(Up);
      Vector3 direction = Vector3.Normalize(LookAt - Position);
      Vector3 left = Vector3.Normalize(Vector3.Cross(Up, direction));
      Vector3 orthoUp = Vector3.Normalize(Vector3.Cross(direction, left));
      var cameraBasis = new Matrix3(left, orthoUp, direction);
      var quat = Quaternion.FromMatrix(cameraBasis);
      return quat;
    }
  }

  public class CameraAutomatic : CameraAnimation {
    float lookAhead;
    Vector3 eyeVertical;
    Vector3 up;

     public CameraAutomatic(Vector3[] positions, Vector3 up, float lookAhead)
    {
      MaxTime = positions.Length - 1 - lookAhead;

      this.lookAhead = lookAhead;
      positionInterpolator = new TrajectoryInterpolator(positions);
      eyeVertical = up.Normalized();
      this.up = up.Normalized();

    }

    public override Matrix4 GetModelViewMatrix (float time)
    {
      // Warning! has side effects (may change eyeVertical vector)

      var target  = GetPosition(time + lookAhead);
      var currentPosition = GetPosition(time);

      if(target == currentPosition)
      {
        // Console.WriteLine("Cannot Compute );
      }

      Vector3 forwardVector = target - GetPosition(time);

      // make eyeVertical orthogonal to forwardVector
      eyeVertical = Vector3.Normalize(eyeVertical - (Vector3.Dot(eyeVertical, Vector3.Normalize(forwardVector)) * Vector3.Normalize(forwardVector)));

      // return eyeVertical to it's original state exponential
      eyeVertical = Vector3.Normalize(eyeVertical + 0.1f * up);

      return Matrix4.LookAt(currentPosition, target, eyeVertical);
    }
  }
  
}
