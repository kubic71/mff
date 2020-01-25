using System;
using System.Collections.Generic;
using MathSupport;
using OpenTK;
using OpenTK.Graphics.OpenGL;
using Utilities;

namespace _086shader
{
  public class AnimatedCamera : DefaultDynamicCamera
  {


    /**
     * AnimatedCamera controls movement and rotation of camera through interpolation of sequence of key-frames.
     * Movement (and orientation) key frames are loaded from exteral script file. 
     *
     * Camera can function in two modes:
     * 
     * 1) automatic camera orientation
     *    - camera is always pointed to where it will be in x seconds, specified by lookAhead=x parameter
     *    - to uniquely determine camera orientation, up vector can be specified, Vector3.UnitY is default
     *    - If camera is looking in almost the same direction as it's up vector, the up vector is orthogonalized as to prevent
     *      abrupt changes in camera orientation. Up vector is returned to it's normal value after a while.
     *      
     * 2) manual camera orientation
     *    - camera orientation key frames are loaded together with position key frames from script file
     *    - orientation key frame is specified by parameters lookAt=[x,y,z] ; up=[x,y,z]
     *    - orientations are internally represented by quaternions and are interpolated using SQUAD
     *
     * 
     * - camera position is specified by pos=[x,y,z]
     *
     *
     * Camera movement scripts are loaded from text file with given format.
     * First line specifies camera orientation mode.
     * In case of auto mode:
     * orientation=auto;up=[x,y,z];lookAhead=x
     *
     * manual mode:
     * orientation=manual
     *
     * Subsequent lines correspond to equally time-spaced keyframes. In auto mode, only position must be specified,
     * whereas manual orientation requires lookAt and up vectors to be specified as well.
     * for example (auto mode):
     *
     * pos=[1,0,0]
     * pos=[2.5,3,4]
     * pos=[5,2,-1.6]
     * pos=[0,2.324,1]
     *
     * manual mode example:
     * pos=[1,0,0];lookAt=[0,1,0];up=[-1,0,0]
     * pos=[-1,0,0];lookAt=[0,0,3];up=[0,1,0]
     * pos=[0,1,1];lookAt=[0.4,1,0];up=[0,1,3]
     * pos=[0,0,0];lookAt=[0,0,1];up=[0,-1,0]
     *
     * Lines starting with // or empty lines are ignored 
     *
     *
     * Whole file might look like this
     * sample_example.cfg:
     * 
     * orientation=auto;up=[0,1,0];lookAhead=1
     * // Dummy comment
     * pos=[1,0,0]
     * pos=[2.5,3,4]
     * pos=[5,2,-1.6]
     * pos=[0,2.324,1]
     * 
     */


    CameraAnimation animation;
    

    /// <summary>
    /// Optional form-data initialization.
    /// </summary>
    /// <param name="name">Return your full name.</param>
    /// <param name="param">Optional text to initialize the form's text-field.</param>
    /// <param name="tooltip">Optional tooltip = param help.</param>
    public static void InitParams (out string name, out string param, out string tooltip)
    {
      // Random paths can be generated like this:
      // var walker = new RandomWalker(5, 100);
      // walker.SaveTo("random5-100.txt");

      name    = "Jakub Hejhal";
      param   = "period=100,start=0";
      tooltip = "period=<cam period in seconds>,start<animation start time (start=0 to play from the beggining)>";
    }

    /// <summary>
    /// Called after form's Param field is changed.
    /// </summary>
    /// <param name="param">String parameters from the form.</param>
    /// <param name="cameraFile">Optional file-name of your custom camera definition (camera script?).</param>
    public override void Update (string param, string cameraFile)
    {
      Dictionary<string, string> p = Util.ParseKeyValueList(param);
      if (p.Count > 0)
      {
        double v = 1.0;
        if (Util.TryParse(p, "period", ref v))
          MaxTime = Math.Max(v, 0.1);
        if (Util.TryParse(p, "start", ref v))
          MinTime= Math.Max(0, v);
      }

      Time = Util.Clamp(Time, MinTime, MaxTime);


      if (cameraFile != null && cameraFile != "")
      {
        animation = CameraScriptLoader.Load(cameraFile);
      }
    }

    /// <param name="param">String parameters from the form.</param>
    /// <param name="cameraFile">Optional file-name of your custom camera definition (camera script?).</param>
    public AnimatedCamera (string param, string cameraFile = "")
    {
      Update(param, cameraFile);
    }

    Matrix4 perspectiveProjection;

    /// <summary>
    /// Returns Projection matrix. Must be implemented.
    /// </summary>
    public override Matrix4 Projection => perspectiveProjection;

    /// <summary>
    /// Called every time a viewport is changed.
    /// It is possible to ignore some arguments in case of scripted camera.
    /// </summary>
    public override void GLsetupViewport (int width, int height, float near, float far)
    {
      // 1. set ViewPort transform:
      GL.Viewport(0, 0, width, height);

      // 2. set projection matrix
      perspectiveProjection = Matrix4.CreatePerspectiveFieldOfView(Fov, width / (float)height, 0.01f, 1000);
      GLsetProjection();
    }

    
    Matrix4 computeModelView ()
    {
      float t = (float) Time % animation.MaxTime;
      return animation.GetModelViewMatrix(t);
    }

    /// <summary>
    /// Crucial property = is called in every frame.
    /// </summary>
    public override Matrix4 ModelView => computeModelView();

    /// <summary>
    /// Crucial property = is called in every frame.
    /// </summary>
    public override Matrix4 ModelViewInv => computeModelView().Inverted();
  }

}
