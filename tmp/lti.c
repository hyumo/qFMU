///////////////////////////////////////////////////////////////////////////////
// 
//  PLEASE DO NOT MODIFY
// 
///////////////////////////////////////////////////////////////////////////////

#include "fmi2Template.h"

#ifdef __cplusplus
extern "C" {
#endif

#define MODEL_IDENTIFIER fmi2model
#define MODEL_GUID "a59da1b2-307c-11ec-8714-00155d4fc7dc"

#define NR 8 
#define NX 2
#define NU 0
#define NY 2

// macro to be used to log messages. The macro check if current 
// log category is valid and, if true, call the logger provided by simulator.
#define FILTERED_LOG(instance, status, categoryIndex, message, ...) if (status == fmi2Error || status == fmi2Fatal || isCategoryLogged(instance, categoryIndex)) \
        instance->functions->logger(instance->functions->componentEnvironment, instance->instanceName, status, \
        logCategoriesNames[categoryIndex], message, ##__VA_ARGS__);

typedef struct {
    ModelState state;
    fmi2Real r[8];
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

#define _X   (comp->r + 0)
#define _DER (comp->r + 2)
#define _X0  (comp->r + 6)
#define _Y   (comp->r + 4)

static const fmi2ValueReference vrs_x[2] = { 0,1 };
static const fmi2ValueReference vrs_der[2] = { 2,3 };
static const fmi2ValueReference vrs_y[2] = { 4,5 };

static const fmi2Real A[2][2] = {
    { 1.0,2.0 },
    { 3.0,4.0 },
};

static const fmi2Real C[2][2] = {
    { 1.0,0.0 },
    { 0.0,1.0 },
};

static const fmi2Real x0_reset[2] = { 0.0,0.0 };

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

/**
 *  \brief Update derivative values
 */
static void updateDerivatives(ModelInstance* comp){
    size_t i = 0;
    for (i = 0; i < NX; i++) {
        fmi2ValueReference der_i = vrs_der[i];
        comp->r[der_i] = innerProduct(A[i], _X, NX);
    }
}

/**
 *  \brief Update states values using numerical integration
 *  \todo TODO: Implement other integration methods
 */
static void updateStates(ModelInstance* comp, fmi2Real h){
    size_t i = 0;
    for (i = 0; i < NX; i++) {
        fmi2ValueReference x_i = vrs_x[i];
        fmi2ValueReference der_i = vrs_y[i];
        // Update states using forward Euler
        comp->r[x_i] += h * comp->r[der_i];
    }
}

/**
 * \brief Update output values based on current state
 */
static void updateOutputs(ModelInstance* comp) {
    size_t i = 0;
    for (i = 0; i < NY; i++){
        fmi2ValueReference y_i = vrs_y[i];
        r(y_i) = 0;
        r(y_i) += innerProduct(C[i], _X, NX);
    }
}

/**
 * \brief Set state initial conditions
 */
static void setX0(ModelInstance* comp) {
    memcpy(_X, _X0, NX*sizeof(fmi2Real));
}

/**
 * \brief ReSet state initial conditions to original values
 */
static void resetX0(ModelInstance* comp){
    memcpy(_X0, x0_reset, NX*sizeof(fmi2Real));
}

/**
 * \brief Set initial input
 */
static void setU0(ModelInstance* comp) {
    memcpy(_U, _U0, NU*sizeof(fmi2Real));
}

/**
 * \brief ReSet input initial conditions to original values
 */
static void resetU0(ModelInstance* comp) {
    memcpy(_U0, u0_reset, NU*sizeof(fmi2Real));
}

/**
 * \brief Update all real values
 */
static void updateAll(ModelInstance* comp) {
    setX0(comp);
    updateDerivatives(comp);
    updateOutputs(comp);
}

/**
 * \brief Reset all parameters i.e. x0, u0
 */
static void resetAll(ModelInstance* comp) {
    resetX0(comp);
}

#include "fmi2Template.c"

#ifdef __cplusplus
}
#endif