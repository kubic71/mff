using OpenTK;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace _086shader
{
  class RandomWalker
  {
    int level;
    int length;
    Vector3 up;
    float lookAhead; 
    TrajectoryScripter scripter;

    public RandomWalker (int level, int length, Vector3 up, float lookAhead)
    {
      this.level = level;
      this.length = length;
      this.up = up;
      this.lookAhead = lookAhead;

      ProduceWalk();
    }

    public RandomWalker (int level, int length) : this(level, length, new Vector3(0, 1, 0), 1)
    {
    }



    void ProduceWalk ()
    {
      int cells = (int)Math.Pow(2, level) - 1;

      // size of the default Hilbert 3D curve model
      float size = 2;


      float step = size / (float)(cells);

      var currentPos = new GridPosition() {X = 0, Y = 0, Z = 0 };
      scripter = new TrajectoryScripter(step);
      int i = 0;
      Random rand = new Random();
      while (true)
      {
        if (i >= length)
          break;
        var randPos = new GridPosition() { X = rand.Next(-cells/2, cells/2), Y = rand.Next(-cells/2, cells/2), Z = rand.Next(-cells/2, cells/2)};

        int farThresh = 3;
        Console.WriteLine(GridPosition.Dist(currentPos, randPos));
        if (Math.Abs(randPos.X - currentPos.X) < farThresh || Math.Abs(randPos.Y - currentPos.Y) < farThresh || Math.Abs(randPos.Z - currentPos.Z) < farThresh)
          continue;

        currentPos = randPos;
        scripter.MoveTo(randPos, step);
        i++;
      }
    }

    public void SaveTo(string filename)
    {
      StreamWriter f =  new StreamWriter(filename);
      f.WriteLine($"orientation=auto;up=[{up.X},{up.Y},{up.Z}];lookAhead={lookAhead}");

      foreach(var p in scripter.OutputTrajectory())
      {
        f.WriteLine($"pos=[{p.X}, {p.Y}, {p.Z}]");
      }

      f.Close();
    }
  }
}
