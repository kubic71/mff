using OpenTK;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace _086shader
{

  /// <summary>
  /// Helps to generate camera trajectory keyframes
  /// </summary>
  class TrajectoryScripter
  {

    List<Vector3> frames;
    public Vector3 currentPosition { get; set; }
    public Vector3 currentDirection { get; set; }
    float Scale;

    public TrajectoryScripter(float scale, Vector3 startingPosition, Vector3 startingDirection)
    {
      frames = new List<Vector3>();
      frames.Add(startingPosition);
      currentDirection = startingDirection;
      currentPosition = startingPosition;
      Scale = scale;
      
      // scale everything by scale
    }

    public TrajectoryScripter(float scale) : this(scale, new Vector3(0, 0, 0), new Vector3(0, 0, 1))
    {
      
    }

    public TrajectoryScripter () : this(1) { }

    public void MoveTo(GridPosition cell, float stepSize)
    {
      Vector3 target = new Vector3(stepSize * cell.X, stepSize * cell.Y, stepSize * cell.Z);
      MoveGradually(new Vector3(target.X, currentPosition.Y, currentPosition.Z));
      MoveGradually(new Vector3(target.X, target.Y, currentPosition.Z));
      MoveGradually(new Vector3(target.X, target.Y, target.Z));
    }

    public void MoveGradually(Vector3 target)
    {
      Vector3 difference = target - currentPosition;
      currentPosition += (difference * 1/2);
      frames.Add(currentPosition);


      float curvature = 0.95f;
      currentPosition += (difference * 1/2) * curvature;
      frames.Add(currentPosition);

      currentPosition += (difference * 1/2) * (1 - curvature);






    }

    public bool MoveOnlyPosition(float amount, Vector3 direction, bool safe = false)
    {
      direction = Vector3.Normalize(direction);
      var oldPosition = currentPosition;
      currentPosition += direction * amount * Scale;

      // went out of SFC
      if (safe && !InSFC())
      {
        currentPosition = oldPosition;
        return false;
      }
      return true;

    }

    public bool Move(float amount, Vector3 direction, bool safe = false)
    {
      Console.WriteLine(direction);
      var oldPosition = currentPosition;
      direction = Vector3.Normalize(direction);

      if (MoveOnlyPosition(amount, direction, safe))
      {
        frames.Add(currentPosition);
        return true;
      } else
      {
        return false;
      }
    }

    public bool InSFC()
    {
      return InSFCRange(currentPosition.X) && InSFCRange(currentPosition.Y) && InSFCRange(currentPosition.Z);
    }

    private bool InSFCRange(float coord)
    {
      // allowed margin around SFC
      float margin = 0;
      return -1 - margin <= coord && coord <= 1 + margin;
    }

    public bool MoveForward(float amount, bool safe=false)
    {
     return Move(amount, currentDirection, safe);
    }

    /// <summary>
    /// Accelerates and deccelerates gradually
    /// </summary>
    /// <param name="amount"></param>
    public bool MoveForwardAccelerateGradually(float amount, bool safe = false)
    {
      // 1/8 3/8 3/8 1/8
      var oldPos = currentPosition;
      bool success = MoveForward(amount * 2/ 8, safe) && MoveForward(amount * 3 / 8, safe) && MoveForward(amount * 5 / 16, safe) && MoveOnlyPosition(amount * 1 / 16, currentDirection, safe);
      if(success)
      {
        return true;
      } else
      {
        currentPosition = oldPos;
        return false;
      }

      /*
      MoveForward(amount * 1/4);
      MoveForward(amount * 1 / 8);
      */
      

    }


    /*
    public void MoveForwardUniformly(float amount)
    {
      MoveForward(amount / 4);
      MoveForward(amount / 4);
      MoveForward(amount / 4);
      MoveForward(amount / 4);
    }

    public void MoveBackward (float amount)
    {
      Move(amount, -currentDirection);
    }
    */

    public void TurnRight()
    {
      currentDirection = new Vector3(-currentDirection.Z, currentDirection.Y, currentDirection.X);
    }

    public void TurnLeft ()
    {
      TurnRight();
      TurnRight();
      TurnRight();
    }


    public bool MoveUp (float amount, bool safe = false)
    {
      return Move(amount, new Vector3(0, 1, 0), safe);
    }

    public bool MoveDown (float amount, bool safe = false)
    {
      return Move(amount, new Vector3(0, -1, 0), safe);
    }

    public Vector3[] OutputTrajectory()
    {
      return frames.ToArray();
      /*
      Vector3[] output = frames.ToArray();
      for(int i = 0; i <= output.Length; i++)
      {
        output[i].X = output[i].X * Scale;
        output[i].Y = output[i].Y * Scale;
        output[i].Z = output[i].Z * ;
      }

      return output;
      */
    }
  }

  class GridPosition
  {
    public static float Dist (GridPosition g1, GridPosition g2)
    {
      return (float)Math.Sqrt((g1.X - g2.X) * (g1.X - g2.X) + (g1.Y - g2.Y) * (g1.Y - g2.Y) + (g1.Z - g2.Z) * (g1.Z - g2.Z));
    }
    public int X { get; set; }
    public int Y { get; set; }
    public int Z { get; set; }

  }
}
