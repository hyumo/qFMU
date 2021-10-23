lti_c_tmpl = r'''///////////////////////////////////////////////////////////////////////////////
// 
//  PLEASE DO NOT MODIFY
// 
///////////////////////////////////////////////////////////////////////////////

#include "fmi2Template.h"

#ifdef __cplusplus
extern "C" {
#endif

#define MODEL_IDENTIFIER {{identifier}}
#define MODEL_GUID "{{guid}}"

#define NR {{nr}} 
#define NX {{nx}}
#define NU {{nu}}
#define NY {{ny}}

// macro to be used to log messages. The macro check if current 
// log category is valid and, if true, call the logger provided by simulator.
#define FILTERED_LOG(instance, status, categoryIndex, message, ...) if (status == fmi2Error || status == fmi2Fatal || isCategoryLogged(instance, categoryIndex)) \
        instance->functions->logger(instance->functions->componentEnvironment, instance->instanceName, status, \
        logCategoriesNames[categoryIndex], message, ##__VA_ARGS__);

typedef struct {
    ModelState state;
    fmi2Real r[{{nr}}];
    fmi2Real time;
    fmi2Char instanceName[256]; // TODO: change 256 by a max_str_len parameter from user argv
    fmi2Type type;
    fmi2String GUID;
    const fmi2CallbackFunctions *functions;
    fmi2Boolean loggingOn;
    fmi2Boolean logCategories[NUMBER_OF_CATEGORIES];
    fmi2ComponentEnvironment componentEnvironment;
    fmi2Boolean isDirtyValues;
} ModelInstance;

static const fmi2String logCategoriesNames[] = {"logAll", "logError", "logFmiCall", "logEvent"};
static ModelInstance instance;
{% if nx>0 %}
#define _X   (comp->r + {{vr0.x}})
#define _DER (comp->r + {{vr0.der}})
#define _X0  (comp->r + {{vr0.x0}})
{%- endif %}
{%- if nu > 0 %}
#define _U   (comp->r + {{vr0.u}})
#define _U0  (comp->r + {{vr0.u0}})
{%- endif %}
{%- if ny>0 %}
#define _Y   (comp->r + {{vr0.y}})
{% endif %}
{%- if nx > 0 %}
static const fmi2ValueReference vrs_x[{{nx}}] = { {{",".join(vrs.x)}} };
static const fmi2ValueReference vrs_der[{{nx}}] = { {{",".join(vrs.der)}} };
{%- endif %}
{%- if ny > 0 %}
static const fmi2ValueReference vrs_y[{{ny}}] = { {{",".join(vrs.y)}} };
{% endif %}
{%- if nx > 0 %}
static const fmi2Real A[{{nx}}][{{nx}}] = {
    {%- for row in A %}
    { {{row}} },
    {%- endfor %}
};
{% endif %}
{%- if nx > 0 and nu > 0 %}
static const fmi2Real B[{{nx}}][{{nu}}] = {
    {%- for row in B %}
    { {{row}} },
    {%- endfor %}
};
{%- endif %}
{%- if nx > 0 and ny > 0 %}
static const fmi2Real C[{{ny}}][{{nx}}] = {
    {%- for row in C %}
    { {{row}} },
    {%- endfor %}
};
{% endif %}
{%- if nu > 0 and ny > 0 %}
static const fmi2Real D[{{ny}}][{{nu}}] = {
    {%- for row in D %}
    { {{row}} },
    {%- endfor %}
};
{% endif %}
{%- if nx > 0 %}
static const fmi2Real x0_reset[{{nx}}] = { {{",".join(x0)}} };
{%- endif %}
{%- if nu > 0 %}
static const fmi2Real u0_reset[{{nu}}] = { {{",".join(u0)}} };
{% endif %}

#ifndef max
#define max(a,b) ((a)>(b) ? (a) : (b))
#endif

///////////////////////////////////////////////////////////////////////////////
// Private functions
///////////////////////////////////////////////////////////////////////////////
static fmi2Boolean isCategoryLogged(ModelInstance *comp, int categoryIndex) {
    if (categoryIndex < NUMBER_OF_CATEGORIES
        && (comp->logCategories[categoryIndex] || comp->logCategories[LOG_ALL])) {
        return fmi2True;
    }
    return fmi2False;
}

static fmi2Boolean isInvalidState(ModelInstance *comp, const char *f, int statesExpected) {
    if (!comp)
        return fmi2True;
    if (!(comp->state & statesExpected)) {
        comp->state = modelError;
        FILTERED_LOG(comp, fmi2Error, LOG_ERROR, "%s: Illegal call sequence.", f)
        return fmi2True;
    }
    return fmi2False;
}

static fmi2Boolean isNullPtr(ModelInstance* comp, const char *f, const char *arg, const void *p) {
    if (!p) {
        comp->state = modelError;
        FILTERED_LOG(comp, fmi2Error, LOG_ERROR, "%s: Invalid argument %s = NULL.", f, arg)
        return fmi2True;
    }
    return fmi2False;
}

static fmi2Boolean isVROutOfRange(ModelInstance *comp, const char *f, fmi2ValueReference vr, int end) {
    if (vr >= end) {
        FILTERED_LOG(comp, fmi2Error, LOG_ERROR, "%s: Illegal value reference %u.", f, vr)
        comp->state = modelError;
        return fmi2True;
    }
    return fmi2False;
}

static fmi2Boolean isInvalidNumber(ModelInstance *comp, const char *f, const char *arg, int n, int nExpected) {
    if (n != nExpected) {
        comp->state = modelError;
        FILTERED_LOG(comp, fmi2Error, LOG_ERROR, "%s: Invalid argument %s = %d. Expected %d.", f, arg, n, nExpected)
        return fmi2True;
    }
    return fmi2False;
}

static fmi2Status unsupportedFunction(fmi2Component c, const char *fName, int statesExpected) {
    ModelInstance *comp = (ModelInstance *)c;
    //fmi2CallbackLogger log = comp->functions->logger;`
    if (isInvalidState(comp, fName, statesExpected))
        return fmi2Error;
    FILTERED_LOG(comp, fmi2OK, LOG_FMI_CALL, fName);
    FILTERED_LOG(comp, fmi2Error, LOG_ERROR, "%s: Function not implemented.", fName)
    return fmi2Error;
}

/**
 * \brief Vector inner product 
 */
static fmi2Real innerProduct(const fmi2Real *v1, const fmi2Real *v2, const size_t n) {
    size_t i = 0.0;
    fmi2Real ret = 0.0;
    for (i = 0; i < n; ++i){
        ret += v1[i]*v2[i];
    }
    return ret;
}

{%- if nx > 0 %}
/**
 *  \brief Update derivative values
 */
static void updateDerivatives(ModelInstance* comp){
    size_t i = 0;
    for (i = 0; i < NX; i++) {
        fmi2ValueReference der_i = vrs_der[i];
        comp->r[der_i] = innerProduct(A[i], _X, NX);
{%- if nu > 0 %}
        comp->r[der_i] += innerProduct(B[i], _U, NU);
{%- endif %}
    }
}
{%- endif %}
{%- if nx > 0 %}
/**
 *  \brief Update states values using numerical integration
 *  \todo TODO: Implement other integration methods
 */
static void updateStates(ModelInstance* comp, fmi2Real h){
    size_t i = 0;
    for (i = 0; i < NX; i++) {
        fmi2ValueReference x_i = vrs_x[i];
        fmi2ValueReference der_i = vrs_der[i];
        // Update states using forward Euler
        comp->r[x_i] += h * comp->r[der_i];
    }
}
{%- endif %}
{%- if ny > 0 %}
/**
 * \brief Update output values based on current state
 */
static void updateOutputs(ModelInstance* comp) {
    size_t i = 0;
    for (i = 0; i < NY; i++){
        fmi2ValueReference y_i = vrs_y[i];
        r(y_i) = 0;
{%- if nx > 0 %}
        r(y_i) += innerProduct(C[i], _X, NX);
{%- endif %}
{%- if nu > 0 %}
        r(y_i) += innerProduct(D[i], _U, NU);
{%- endif %}
    }
}
{%- endif %}
{%- if nx > 0 %}
static void copyX0toX(ModelInstance* comp){
    memcpy(_X, _X0, NX*sizeof(fmi2Real));
}
/**
 * \brief ReSet state initial conditions to original values
 */
static void resetX(ModelInstance* comp){
    memcpy(_X0, x0_reset, NX*sizeof(fmi2Real));
    copyX0toX(comp);
}
{%- endif %}
{%- if nu > 0 %}
static void copyU0toU(ModelInstance* comp) {
    memcpy(_U, _U0, NU*sizeof(fmi2Real));
}
/**
 * \brief ReSet input initial conditions to original values
 */
static void resetU(ModelInstance* comp) {
    memcpy(_U0, u0_reset, NU*sizeof(fmi2Real));
    copyU0toU(comp);
}
{%- endif %}


static void evaluate(ModelInstance* comp){
{%- if nx > 0 %}
    updateDerivatives(comp);
{%- endif %}
{%- if ny > 0 %}
    updateOutputs(comp);
{%- endif %}
}


#include "fmi2Template.c"

#ifdef __cplusplus
}
#endif
'''

lti_md_xml_tmpl = r'''<?xml version="1.0" encoding="UTF-8"?>
<fmiModelDescription
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  fmiVersion="2.0"
  modelName="{{identifier}}"
  guid="{{guid}}"
  version="{{version}}"
  generationTool="qfmu"
  generationDateAndTime="{{datetime}}"
  numberOfEventIndicators="0">

  <ModelExchange
    modelIdentifier="{{identifier}}"
    canGetAndSetFMUstate="false"
    canSerializeFMUstate="false"
    providesDirectionalDerivative="false">
    <SourceFiles>
      <File
        name="fmi2model.c"/>
    </SourceFiles>
  </ModelExchange>

  <CoSimulation
    modelIdentifier="{{identifier}}"
    canHandleVariableCommunicationStepSize="false"
    canNotUseMemoryManagementFunctions="false"
    canGetAndSetFMUstate="false"
    canSerializeFMUstate="false">
    <SourceFiles>
      <File name="fmi2model.c"/>
    </SourceFiles>
  </CoSimulation>

  <LogCategories>
    <Category name="logAll"/>
    <Category name="logError"/>
    <Category name="logFmiCall"/>
    <Category name="logEvent"/>
  </LogCategories>

  <DefaultExperiment startTime="0.0"
    stopTime="1.0"
    tolerance="0.0001"/>
  
  <ModelVariables>
    {%- for i in range(nx) %}
    <ScalarVariable name="x{{i+1}}" valueReference="{{vrs.x[i]}}" description="Continuous state {{i+1}}">
      <Real/>
    </ScalarVariable>
    {%- endfor %}
    {%- for i in range(nx) %}
    <ScalarVariable name="der_x{{i+1}}" valueReference="{{vrs.der[i]}}" description="State derivative {{i+1}}">
      <Real derivative="{{ i+1 }}"/>
    </ScalarVariable>
    {%- endfor %}
    {%- for i in range(nu) %}
    <ScalarVariable name="u{{i+1}}" valueReference="{{vrs.u[i]}}" description="Model input {{i+1}}" causality="input">
      <Real start="{{u0[i]}}"/>
    </ScalarVariable>
    {%- endfor %}
    {%- for i in range(ny) %}
    <ScalarVariable name="y{{i+1}}" valueReference="{{vrs.y[i]}}" description="Model output {{i+1}}" causality="output">
      <Real/>
    </ScalarVariable>
    {%- endfor %}
    {%- for i in range(nx) %}
    <ScalarVariable name="x{{i+1}}_start" valueReference="{{vrs.x0[i]}}" description="Start value for x{{i+1}}" causality="parameter" variability="fixed">
      <Real start="{{x0[i]}}"/>
    </ScalarVariable>
    {%- endfor %}
    {%- for i in range(nu) %}
    <ScalarVariable name="u{{i+1}}_start" valueReference="{{vrs.u0[i]}}" description="Start value for u{{i+1}}" causality="parameter" variability="fixed">
      <Real start="{{u0[i]}}"/>
    </ScalarVariable>
    {%- endfor %}
  </ModelVariables>
  
  <ModelStructure>
    <Outputs>
    {%- for i in range(ny) %}
      <Unknown index="{{vr0.y + i + 1}}" />
    {%- endfor %}
    </Outputs>
    <Derivatives>
    {%- for i in range(nx) %}
      <Unknown index="{{vr0.der + i + 1}}" />
    {%- endfor %}
    </Derivatives>
  </ModelStructure>
</fmiModelDescription>
'''