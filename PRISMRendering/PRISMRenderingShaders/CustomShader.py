#@file CustomShader.py

import imp
import sys
import inspect
import os
import importlib.util
import math  
import vtk, qt, ctk, slicer

"""CustomShader Class containing the function to access the parameters of the shader.
Generic Custom Shader
""" 
class CustomShader():
  
  ## Integers parameters of the shader
  shaderfParams = {}
  ## Booleans parameters of the shader
  shaderiParams = {}
  ## Transfer Functions parameters of the shader 
  shader4fParams = {}
  ## Floats parameters of the shader
  shaderbParams = {}
  ## Points parameters of the shader
  shaderrParams = {}
  ## Ranges parameters of the shader 
  shadertfParams = {}
  ## Volumes parameters of the shader 
  shadervParams = {}

  def __init__(self, shaderPropertyNode, volumeNode = None):
    assert shaderPropertyNode != None, 'CustomShader: a valid shader property node must provided to the constructor'
    ## Property node of the shader
    self.shaderPropertyNode = shaderPropertyNode
    ## Properies of the shader
    self.shaderProperty = shaderPropertyNode.GetShaderProperty()
    ## Uniforms of the shader
    self.shaderUniforms = self.shaderPropertyNode.GetFragmentUniforms()

    ## Floats parameters of the shader
    self.paramfValues = {}
    ## Integers parameters of the shader
    self.paramiValues = {}
    ## Points parameters of the shader
    self.param4fValues = {}
    ## Booleans parameters of the shader
    self.parambValues = {}
    ## Ranges parameters of the shader 
    self.paramrValues = {}
    ## Transfer Functions parameters of the shader 
    self.paramtfValues = {}
    ## Volumes parameters of the shader 
    self.paramvValues = {}

    for p in self.shaderfParams.keys():
      self.paramfValues[p] = self.shaderfParams[p]['defaultValue']
    for p in self.shaderiParams.keys():
      self.paramiValues[p] = self.shaderiParams[p]['defaultValue']
    for p in self.shader4fParams.keys():
      self.param4fValues[p] = self.shader4fParams[p]['defaultValue']   
    for p in self.shaderbParams.keys():
      self.parambValues[p] = self.shaderbParams[p]['defaultValue']   
    for p in self.shaderrParams.keys():
      self.paramrValues[p] = self.shaderrParams[p]['defaultValue']  
    for p in self.shadertfParams.keys():
      self.paramtfValues[p] = self.shadertfParams[p]['defaultColors']  
    for p in self.shadervParams.keys():
      self.paramvValues[p] = self.shadervParams[p]['defaultVolume']  
    

  @classmethod
  def InstanciateCustomShader(cls, shaderDisplayName, shaderPropertyNode, volumeNode):
    """Function to instanciate a custom shader.

    :param shaderDisplayName: Display name of the shader. 
    :type shaderDisplayName: str
    :param shaderPropertyNode: Shader property node. 
    :type shaderPropertyNode: vtkMRMLShaderPropertyNode
    :param volumeNode: Current volume.
    :type volumeNode: vtkMRMLScalarVolumeNode
    """
    if shaderDisplayName == cls.GetDisplayName():
      return CustomShader(shaderPropertyNode, volumeNode)

    for c in cls.allClasses:
      if c.GetDisplayName() == shaderDisplayName:
        return c(shaderPropertyNode, volumeNode)
    return None

  @classmethod
  def GetAllShaderClassNames(cls):
    """Function to get the class names of all of the shaders.

    :return: Names of all the classes. 
    :rtype: array[str]

    """
    allNames = [] #names of shaders
    # Classes of shaders
    cls.allClasses = []

    #get path of package
    packageName = 'PRISMRenderingShaders'
    f, filename, description = imp.find_module(packageName)
    package = imp.load_module(packageName, f, filename, description)
    csPath = os.path.dirname(package.__file__).replace("\\", "/")

    csClass = getattr(sys.modules[__name__], "CustomShader") # Custom shader class
    
    #find python files in directory
    for dirpath, _, filenames in os.walk(csPath):
      for filename in filenames:
        filename, file_extension = os.path.splitext(dirpath+"/"+filename)
        if file_extension == ".py":
          
          #load the module and save it
          dirpath, filename = os.path.split(filename + file_extension)
          loader = importlib.machinery.SourceFileLoader(filename, dirpath+"/"+filename)
          spec = importlib.util.spec_from_loader(loader.name, loader)
          mod = importlib.util.module_from_spec(spec)
          loader.exec_module(mod)

          #check if module is subclass of CustomShader
          currentModule = inspect.getmembers(mod, inspect.isclass)
          if (len(currentModule)) > 1 :
            m1 = currentModule[0][1]
            m2 = currentModule[1][1]
            if issubclass(m1, csClass) and (m1 != csClass ) :
              cls.allClasses.append(m1)
              allNames.append( m1.GetDisplayName()) 
            elif issubclass(m2, csClass) and (m2 != csClass ):
              cls.allClasses.append(m2)
              allNames.append( m2.GetDisplayName() )
    allNames.append( cls.GetDisplayName() )
    
    return allNames

  @classmethod
  def GetDisplayName(cls):
    """Function to get the name of the current class.
    
    :return: Name of the current class.
    :rtype: str
    """
    return 'None'
  
  @classmethod
  def GetClassName(cls, shaderDisplayName):
    """Function to get a class from it's display name.

    :return: Class.
    :rtype: cls
    """
    if shaderDisplayName == cls.GetDisplayName():
      return CustomShader
    
    if not hasattr(cls, "allClasses"):
      cls.GetAllShaderClassNames()
    for c in cls.allClasses:
      if c.GetDisplayName() == shaderDisplayName:
        return c
    return None
  
  @classmethod
  def GetClass(cls, shaderName):
    """Function to get a class from it's name.

    :return: Class.
    :rtype: cls
    """
    if shaderName == cls.__name__:
      return CustomShader
  
    if not hasattr(cls, "allClasses"):
      cls.GetAllShaderClassNames()
    for c in cls.allClasses:
      if c.__name__ == shaderName:
        return c
    return None

  @classmethod
  def hasShaderParameter(cls, name, paramType):
    """Function to check if a parameter is in the shader.

    :param name: Name of the parameter. 
    :type name: str
    :param paramType: Type of the parameter. 
    :type paramType: str
    :return: Parameter is in the shader. 
    :rtype: bool
    """
    if paramType == float :
      return name in cls.shaderfParams
    elif paramType == int :
      return name in cls.shaderiParams

  def getVolumeRange(self):
    """Function to get the range of the current volume.

    :return: Range of the current volume. 
    :rtype: float.
    """
    pass

  def getParameterNames(self):
    """Function to get the shader parameter names.

    :return: Shader parameter names. 
    :rtype: array[str]
    """
    return []

  def getShaderPropertyNode(self):
    """Function to get the shader property node of the shader.

    :return: Property node of the shader. 
    :rtype: vtkMRMLShaderPropertyNode
    """
    return self.shaderPropertyNode

  def setupShader(self):
    """Function to setup the shader.

    """
    self.clear()
    self.setAllUniforms()

  def setPathEnds(self,entry,target):
    pass

  def setAllUniforms(self):
    """Function to set the uniforms of the shader.

    """
    for p in self.paramfValues.keys():
      self.shaderUniforms.SetUniformf(p, self.paramfValues[p])

    for p in self.paramiValues.keys():
      self.shaderUniforms.SetUniformi(p, int(self.paramiValues[p]))

    for p in self.parambValues.keys():
      self.shaderUniforms.SetUniformi(p, int(self.parambValues[p]))

    for p in self.param4fValues.keys():
      x = self.param4fValues.get(p).get('x')
      y = self.param4fValues.get(p).get('y')
      z = self.param4fValues.get(p).get('z')
      w = self.param4fValues.get(p).get('w')
      self.shaderUniforms.SetUniform4f(p, [x, y, z , w])
    
    for p in self.paramrValues.keys():
      self.shaderUniforms.SetUniformf(p+ "Min", int(self.paramrValues[p][0]))
      self.shaderUniforms.SetUniformf(p+ "Max", int(self.paramrValues[p][1]))

  def setShaderParameter(self, paramName, paramValue, paramType):
    """Function to set the parameters of the shader.

    :param paramName: Name of the parameter. 
    :type paramName: str
    :param paramType: Type of the parameter. 
    :type paramType: str
    :param paramValue: Value of the parameter.
    :type paramValue: int|float|str
    """
    if paramType == float :
      p = self.paramfValues.get(paramName)
      if p != None:
        self.paramfValues[paramName] = paramValue
        self.shaderUniforms.SetUniformf(paramName, paramValue)

    elif paramType == int :
      p = self.paramiValues.get(paramName)
      if p != None:
        self.paramiValues[paramName] = paramValue
        self.shaderUniforms.SetUniformi(paramName, int(paramValue))
    
    elif paramType == "markup":
      p = self.param4fValues.get(paramName)
      if p != None:
        self.param4fValues[paramName] = paramValue
        self.shaderUniforms.SetUniform4f(paramName, paramValue)

    elif paramType == "bool":
      p = self.parambValues.get(paramName)
      if p != None:
        self.param4fValues[paramName] = paramValue
        self.shaderUniforms.SetUniformi(paramName, int(paramValue))
    elif paramType == "range" :
      p = self.paramrValues.get(paramName)
      if p != None:
        self.paramrValues[paramName] = paramValue
        self.shaderUniforms.SetUniformf(paramName+ "Min", paramValue[0])
        self.shaderUniforms.SetUniformf(paramName+ "Max", paramValue[1])

  def getShaderParameter(self, paramName, paramType):
    """Function to get the parameters of the shader.
    
    :param paramName: Name of the parameter. 
    :type paramName: str
    :param paramType: Type of the parameter. 
    :type paramType: str
    :return: Value of the parameter. 
    :rtype: int|float|str
    """
    if paramType == float :
      return self.paramfValues.get(paramName)
    if paramType == int :
      return self.paramiValues.get(paramName)

  def clear(self):
    """Function to clear the shader.

    """
    self.shaderUniforms.RemoveAllUniforms()
    self.shaderProperty.ClearAllFragmentShaderReplacements()