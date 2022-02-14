using System;
using System.Collections.Generic;
using System.Drawing;
using LineCanvas;
using MathSupport;
using Utilities;

namespace _093animation
{
  public class Animation
  {
    static List<List<Line>> hilbertCache;
    static int SCREEN_SIZE = 1024;
    static int SEQUENCE_LENGHT = 10;

    /// <summary>
    /// Form data initialization.
    /// </summary>
    /// <param name="name">Your first-name and last-name.</param>
    /// <param name="wid">Image width in pixels.</param>
    /// <param name="hei">Image height in pixels.</param>
    /// <param name="from">Animation start in seconds.</param>
    /// <param name="to">Animation end in seconds.</param>
    /// <param name="fps">Frames-per-seconds.</param>
    /// <param name="param">Optional text to initialize the form's text-field.</param>
    /// <param name="tooltip">Optional tooltip = param help.</param>
    public static void InitParams (out string name, out int wid, out int hei, out double from, out double to, out double fps, out string param, out string tooltip)
    {
      // {{

      // Put your name here.
      name = "Jakub Hejhal";

      // Image size in pixels.
      wid = SCREEN_SIZE;
      hei = SCREEN_SIZE;

      // Animation.
      from = 0.0;
      to =  30.0;
      fps = 60.0;

      // Specific animation params.
      param = "width=2.0,anti=true";

      // Tooltip = help.
      tooltip = "width=<double>, anti[=<bool>]";

      // }}
    }


    struct Line
    {
      public double x1;
      public double y1;
      public double x2;
      public double y2;
    }

    class Rotater
    {
      private double anchorX;
      private double anchorY;
      private double width;
      private int rotation;

      public Rotater (double anchorX, double anchorY, double width, int rotation)
      {
        this.anchorX = anchorX;
        this.anchorY = anchorY;
        this.width = width;
        this.rotation = rotation;
      }

      // x and y must be between 0 and 1
      public void Transform (double x, double y, out double transX, out double transY)
      {

        if (rotation == 0)
        {
          //  ---
          // |   |

          // do nothing
        }
        else if (rotation == 1)
        {   // ---
            //    |
            // ---
          double tmp = x;
          x = y;
          y = -tmp;
          y += 1;
        }
        else if (rotation == 2)
        {
          x = -x + 1;
          y = -y + 1;

        }
        else if (rotation == 3)
        {
          double tmp = x;
          x = -y;
          y = tmp;
          x += 1;
        }

        transX = anchorX + x * width;
        transY = anchorY + y * width;

      }

      public Line Transform (Line line)
      {
        Line l = new Line();
        Transform(line.x1, line.y1, out l.x1, out l.y1);
        Transform(line.x2, line.y2, out l.x2, out l.y2);
        return l;
      }
    }



    /// <summary>
    /// Global initialization. Called before each animation batch
    /// or single-frame computation.
    /// </summary>
    /// <param name="width">Width of the future canvas in pixels.</param>
    /// <param name="height">Height of the future canvas in pixels.</param>
    /// <param name="start">Start time (t0)</param>
    /// <param name="end">End time (for animation length normalization).</param>
    /// <param name="fps">Required fps.</param>
    /// <param name="param">Optional string parameter from the form.</param>
    public static void InitAnimation (int width, int height, double start, double end, double fps, string param)
    {
      InitCache(end);
    }

    private static void InitCache(double time_end)
    {
      int N = (int)Math.Ceiling(time_end / SEQUENCE_LENGHT) + 1 ;
      hilbertCache = new List<List<Line>>();
      for (int i = 0; i <= N; i++)
      {
        hilbertCache.Add(MakeHilbertCurve(i));
      }
    }


    /// <summary>
    /// Draw single animation frame.
    /// Has to be re-entrant!
    /// </summary>
    /// <param name="c">Canvas to draw to.</param>
    /// <param name="time">Current time in seconds.</param>
    /// <param name="start">Start time (t0)</param>
    /// <param name="end">End time (for animation length normalization).</param>
    /// <param name="param">Optional string parameter from the form.</param>
    public static void DrawFrame (Canvas c, double time, double start, double end, string param)
    {
      

      // input params:
      float penWidth = 1.0f;   // pen width
      bool antialias = true;  // use anti-aliasing?

      Dictionary<string, string> p = Util.ParseKeyValueList(param);
      if (p.Count > 0)
      {
        // with=<line-width>
        if (Util.TryParse(p, "width", ref penWidth))
        {
          if (penWidth < 0.0f)
            penWidth = 0.0f;
        }

        // anti[=<bool>]
        Util.TryParse(p, "anti", ref antialias);

        c.Clear(Color.Black);

        // 1st quadrant - star.
        c.SetPenWidth(penWidth);
        c.SetAntiAlias(antialias);
      }

      int order = (int)time / SEQUENCE_LENGHT + 1;
      double norm = (time % SEQUENCE_LENGHT) / SEQUENCE_LENGHT;

      double norm2;
      if (norm < 0.2)
      {
        norm2 = Smooth(norm / 0.2);
        DrawHilbertCurveToCanvas(c, hilbertCache[order], 0, 0, (int)(SCREEN_SIZE * (1 - norm2 / 2)));
      } else if (norm < 0.4)
      {
        norm2 = Smooth((norm - 0.2) / 0.2);

        c.SetColor(Color.White);
        DrawHilbertCurveToCanvas(c, hilbertCache[order], 0, 0, SCREEN_SIZE / 2 );

        int intensity = (int)(255 * norm2);
        c.SetColor(Color.FromArgb(intensity, intensity, intensity));
        DrawHilbertCurveToCanvas(c, hilbertCache[order], 0, SCREEN_SIZE / 2, SCREEN_SIZE / 2);
        DrawHilbertCurveToCanvas(c, hilbertCache[order], SCREEN_SIZE / 2, 0, SCREEN_SIZE / 2);
        DrawHilbertCurveToCanvas(c, hilbertCache[order], SCREEN_SIZE / 2,  SCREEN_SIZE / 2, SCREEN_SIZE / 2);
      } else if (norm < 0.6)
      {
        norm2 = Smooth((norm - 0.4) / 0.2);
        c.SetColor(Color.White);
        DrawHilbertCurveToCanvas(c, hilbertCache[order], 0, SCREEN_SIZE / 2, SCREEN_SIZE / 2);
        DrawHilbertCurveToCanvas(c, hilbertCache[order], SCREEN_SIZE / 2, 0, SCREEN_SIZE / 2);
        DrawHilbertCurveToCanvas(c, hilbertCache[order], SCREEN_SIZE / 2, SCREEN_SIZE / 2, SCREEN_SIZE / 2);
        DrawHilbertCurveToCanvas(c, RotateCurve(hilbertCache[order], - 90 * norm2), 0, 0, SCREEN_SIZE / 2);

      } else if (norm < 0.8)
      {
        norm2 = Smooth((norm - 0.6) / 0.2);
        c.SetColor(Color.White);
        DrawHilbertCurveToCanvas(c, RotateCurve(hilbertCache[order], -90), 0, 0, SCREEN_SIZE / 2);
        DrawHilbertCurveToCanvas(c, hilbertCache[order], 0, SCREEN_SIZE / 2, SCREEN_SIZE / 2);
        DrawHilbertCurveToCanvas(c, RotateCurve(hilbertCache[order], 90 * norm2), SCREEN_SIZE / 2, 0, SCREEN_SIZE / 2);
        DrawHilbertCurveToCanvas(c, hilbertCache[order], SCREEN_SIZE / 2, SCREEN_SIZE / 2, SCREEN_SIZE / 2);

      } else
      {
        norm2 = Smooth((norm - 0.8) / 0.2);
        c.SetColor(Color.White);
        DrawHilbertCurveToCanvas(c, RotateCurve(hilbertCache[order], -90), 0, 0, SCREEN_SIZE / 2);
        DrawHilbertCurveToCanvas(c, hilbertCache[order], 0, SCREEN_SIZE / 2, SCREEN_SIZE / 2);
        DrawHilbertCurveToCanvas(c, RotateCurve(hilbertCache[order], 90), SCREEN_SIZE / 2, 0, SCREEN_SIZE / 2);
        DrawHilbertCurveToCanvas(c, hilbertCache[order], SCREEN_SIZE / 2, SCREEN_SIZE / 2, SCREEN_SIZE / 2);


        double distanceFromEdge = 1 / Math.Pow(2, order + 2);
        c.SetColor(Color.FromArgb(255, (int)(255 * norm2), (int)(255 * norm2)));
        c.Line(SCREEN_SIZE * distanceFromEdge, SCREEN_SIZE * (0.5 - distanceFromEdge), SCREEN_SIZE * distanceFromEdge, SCREEN_SIZE * (0.5 - distanceFromEdge + 2 * distanceFromEdge * norm2));
        c.Line(SCREEN_SIZE * (1 - distanceFromEdge), SCREEN_SIZE * (0.5 + distanceFromEdge), SCREEN_SIZE * (1 - distanceFromEdge), SCREEN_SIZE * (0.5 + distanceFromEdge - 2 * distanceFromEdge * norm2));
        c.Line(SCREEN_SIZE * (0.5 - distanceFromEdge), SCREEN_SIZE * (0.5 + distanceFromEdge), SCREEN_SIZE * (0.5 - distanceFromEdge + 2 * distanceFromEdge * norm2), SCREEN_SIZE * (0.5 + distanceFromEdge));

      }


    }


    private static double Smooth(double norm)
    {
      // shifted sigmoid
      double sharpness = 15;
      return 1 / (1 + Math.Exp(-sharpness * (norm - 0.5)));
    }

    private static List<Line> RotateCurve(List<Line> curve, double angle)
    {
      List<Line> rotatedLines = new List<Line>();
      // rotate around center at (0.5, 0.5) conter clockwise
      foreach(var line in curve)
      {
        Line rotLine = new Line();
        RotatePoint(line.x1, line.y1, angle, out rotLine.x1, out rotLine.y1);
        RotatePoint(line.x2, line.y2, angle, out rotLine.x2, out rotLine.y2);

        rotatedLines.Add(rotLine);
      }

      return rotatedLines;
    }

    private static void RotatePoint(double x, double y, double angle, out double rotX, out double rotY)
    {

      angle = Arith.DegreeToRadian(angle);
      // rotate around center at (0.5, 0.5) conter clockwise
      x -= 0.5;
      y -= 0.5;
      double xTmp = x;
      x = x * Math.Cos(angle) - y * Math.Sin(angle);
      y = xTmp * Math.Sin(angle) + y * Math.Cos(angle);
      rotX = x += 0.5;
      rotY = y += 0.5;
    }


    private static List<Line> MakeHilbertCurve (int order)
    {
      List<Line> curve = new List<Line>();
      MakeHilbert(curve, 0, 0, 1, order, 0);
      return curve;
    }

    private static void MakeHilbert (List<Line> curve, double x, double y, double width, int order, int rotation)
    {
      if (order < 1)
        return;

      Rotater rotater = new Rotater(x, y, width, rotation);
      double distanceFromEdge = 1 / Math.Pow(2, order + 1);

      double transX;
      double transY;

      rotater.Transform(0.25, 0.25, out transX, out transY);
      MakeHilbert(curve, transX - width / 4, transY - width / 4, width / 2, order - 1, (rotation + 1) % 4);
      curve.Add(rotater.Transform(new Line()
      {
        x1 = distanceFromEdge,
        y1 = 0.5 - distanceFromEdge,
        x2 = distanceFromEdge,
        y2 = 0.5 + distanceFromEdge
      }));

      rotater.Transform(0.25, 0.75, out transX, out transY);
      MakeHilbert(curve, transX - width / 4, transY - width / 4, width / 2, order - 1, rotation);
      curve.Add(rotater.Transform(new Line()
      {
        x1 = 0.5 - distanceFromEdge,
        y1 = 0.5 + distanceFromEdge,
        x2 = 0.5 + distanceFromEdge,
        y2 = 0.5 + distanceFromEdge
      }));

      rotater.Transform(0.75, 0.75, out transX, out transY);
      MakeHilbert(curve, transX - width / 4, transY - width / 4, width / 2, order - 1, rotation);
      curve.Add(rotater.Transform(new Line()
      {
        x1 = 1 - distanceFromEdge,
        y1 = 0.5 + distanceFromEdge,
        x2 = 1 - distanceFromEdge,
        y2 = 0.5 - distanceFromEdge
      }));

      rotater.Transform(0.75, 0.25, out transX, out transY);
      MakeHilbert(curve, transX - width / 4, transY - width / 4, width / 2, order - 1, (rotation + 3) % 4);
    }


    private static void DrawHilbertCurveToCanvas (Canvas c, List<Line> curve, int x, int y, int size)
    {
      foreach(var line in curve)
      {
        c.Line(x + line.x1 * size, y + line.y1 * size, x + line.x2 * size, y + line.y2 * size);
      }
    }
  }

}
