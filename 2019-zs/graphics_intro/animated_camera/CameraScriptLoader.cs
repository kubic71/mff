using OpenTK;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Utilities;

namespace _086shader
{
  public static class CameraScriptLoader
  {

    static Vector3 ParseVector(string vecstr)
    {
      // [x, y, z]
      var coords = vecstr.Replace("[", "").Replace("]", "").Replace(" ", "").Split(',');
      return new Vector3(float.Parse(coords[0]), float.Parse(coords[1]), float.Parse(coords[2]));
    }

     static Vector3 ParseVector(Dictionary<string, string> d, string key)
    {
      return ParseVector(d[key]);
    }


    static void DuplicateEnds(List<Vector3> list)
    {
      list.Insert(0, list[0]);
      list.Insert(list.Count, list[list.Count - 1]);
    }

    private static string ReadLine(StreamReader reader)
    {
      // StreamReader adapter that skips comments

      string line;
      while(true)
      {
        line = reader.ReadLine();
        if (line == null)
          return null;

        line = line.Replace(" ", "");
        if (line.StartsWith("//") || line == "")
          continue;

        return line;
      }
    }

    public static CameraAnimation Load(string filename)
    {
      StreamReader reader = new StreamReader(filename);

      Dictionary<string, string> p = Util.ParseKeyValueList(ReadLine(reader), ';');


      
      if(p["orientation"]  == "auto")
      {
        // default values
        float lookAhead = 1;
        Vector3 up = new Vector3(0, 1, 0);


        if (p.ContainsKey("lookAhead"))
          lookAhead = float.Parse(p["lookAhead"]);

        if (p.ContainsKey("up"))
        { // up=[x,y,z]
          up = ParseVector(p["up"]);
        }

        string line;
        List<Vector3> positions = new List<Vector3>();
        while((line=ReadLine(reader)) != null)
        {
          var dict = Util.ParseKeyValueList(line, ';');
          positions.Add(ParseVector(dict, "pos"));
        }

        reader.Close();


        return new CameraAutomatic(positions.ToArray(), up, lookAhead);

      } else
      {
        // manual camera

        // each line look like this:
        // pos =[1, 0, 0],lookAt =[0, 1, 0],up =[-1, 0, 0]
        string line;
        List<Vector3> positions = new List<Vector3>();
        List<Vector3> lookAts = new List<Vector3>();
        List<Vector3> Ups = new List<Vector3>();

        while ((line = ReadLine(reader)) != null)
        {
          var dict = Util.ParseKeyValueList(line, ';');
          positions.Add(ParseVector(dict, "pos"));
          lookAts.Add(ParseVector(dict, "lookAt"));
          Ups.Add(ParseVector(dict, "up"));
        }


        reader.Close();
        return new CameraManual(positions.ToArray(), lookAts.ToArray(), Ups.ToArray());
      }
    }
  }
}
