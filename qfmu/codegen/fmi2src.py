###############################################################################
# fmi2Template.h
###############################################################################
fmi2Template_h = r'''/* ---------------------------------------------------------------------------*
 * fmuTemplate.h
 * Definitions by the includer of this file
 * Copyright QTronic GmbH. All rights reserved.
 * ---------------------------------------------------------------------------
 * Modified by Hang Yu
 * ---------------------------------------------------------------------------*/

#include <stdio.h>
#include <string.h>
#include <assert.h>

// C-code FMUs have functions names prefixed with MODEL_IDENTIFIER_.
// Define DISABLE_PREFIX to build a binary FMU.
#ifndef DISABLE_PREFIX
#define pasteA(a,b)     a ## b
#define pasteB(a,b)    pasteA(a,b)
#define FMI2_FUNCTION_PREFIX pasteB(MODEL_IDENTIFIER, _)
#endif
#include "fmi2Functions.h"

#ifdef __cplusplus
extern "C" {
#endif

// macros used to define variables
#define  r(vr) comp->r[vr]

// categories of logging supported by model.
// Value is the index in logCategories of a ModelInstance.
#define LOG_ALL       0
#define LOG_ERROR     1
#define LOG_FMI_CALL  2
#define LOG_EVENT     3

#define NUMBER_OF_CATEGORIES 4

typedef enum {
    modelStartAndEnd        = 1<<0,
    modelInstantiated       = 1<<1,
    modelInitializationMode = 1<<2,

    // ME states
    modelEventMode          = 1<<3,
    modelContinuousTimeMode = 1<<4,
    // CS states
    modelStepComplete       = 1<<5,
    modelStepInProgress     = 1<<6,
    modelStepFailed         = 1<<7,
    modelStepCanceled       = 1<<8,

    modelTerminated         = 1<<9,
    modelError              = 1<<10,
    modelFatal              = 1<<11,
} ModelState;

// ---------------------------------------------------------------------------
// Function calls allowed state masks for both Model-exchange and Co-simulation
// ---------------------------------------------------------------------------
#define MASK_fmi2GetTypesPlatform        (modelStartAndEnd | modelInstantiated | modelInitializationMode | modelEventMode | modelContinuousTimeMode | modelStepComplete | modelStepInProgress | modelStepFailed | modelStepCanceled | modelTerminated | modelError)
#define MASK_fmi2GetVersion              MASK_fmi2GetTypesPlatform
#define MASK_fmi2SetDebugLogging         (modelInstantiated | modelInitializationMode | modelEventMode | modelContinuousTimeMode | modelStepComplete | modelStepInProgress | modelStepFailed | modelStepCanceled | modelTerminated | modelError)
#define MASK_fmi2Instantiate             (modelStartAndEnd)
#define MASK_fmi2FreeInstance            (modelInstantiated | modelInitializationMode | modelEventMode | modelContinuousTimeMode | modelStepComplete | modelStepFailed | modelStepCanceled | modelTerminated | modelError)
#define MASK_fmi2SetupExperiment         modelInstantiated
#define MASK_fmi2EnterInitializationMode modelInstantiated
#define MASK_fmi2ExitInitializationMode  modelInitializationMode
#define MASK_fmi2Terminate               (modelEventMode | modelContinuousTimeMode | modelStepComplete | modelStepFailed)
#define MASK_fmi2Reset                   MASK_fmi2FreeInstance
#define MASK_fmi2GetReal                 (modelInitializationMode | modelEventMode | modelContinuousTimeMode | modelStepComplete | modelStepFailed | modelStepCanceled | modelTerminated | modelError)
#define MASK_fmi2GetInteger              MASK_fmi2GetReal
#define MASK_fmi2GetBoolean              MASK_fmi2GetReal
#define MASK_fmi2GetString               MASK_fmi2GetReal
#define MASK_fmi2SetReal                 (modelInstantiated | modelInitializationMode | modelEventMode | modelContinuousTimeMode | modelStepComplete)
#define MASK_fmi2SetInteger              (modelInstantiated | modelInitializationMode | modelEventMode | modelStepComplete)
#define MASK_fmi2SetBoolean              MASK_fmi2SetInteger
#define MASK_fmi2SetString               MASK_fmi2SetInteger
#define MASK_fmi2GetFMUstate             MASK_fmi2FreeInstance
#define MASK_fmi2SetFMUstate             MASK_fmi2FreeInstance
#define MASK_fmi2FreeFMUstate            MASK_fmi2FreeInstance
#define MASK_fmi2SerializedFMUstateSize  MASK_fmi2FreeInstance
#define MASK_fmi2SerializeFMUstate       MASK_fmi2FreeInstance
#define MASK_fmi2DeSerializeFMUstate     MASK_fmi2FreeInstance
#define MASK_fmi2GetDirectionalDerivative (modelInitializationMode | modelEventMode | modelContinuousTimeMode | modelStepComplete | modelStepFailed | modelStepCanceled | modelTerminated | modelError)

// ---------------------------------------------------------------------------
// Function calls allowed state masks for Model-exchange
// ---------------------------------------------------------------------------
#define MASK_fmi2EnterEventMode          (modelEventMode | modelContinuousTimeMode)
#define MASK_fmi2NewDiscreteStates       modelEventMode
#define MASK_fmi2EnterContinuousTimeMode modelEventMode
#define MASK_fmi2CompletedIntegratorStep modelContinuousTimeMode
#define MASK_fmi2SetTime                 (modelInstantiated | modelEventMode | modelContinuousTimeMode)
#define MASK_fmi2SetContinuousStates     (modelEventMode | modelContinuousTimeMode) //modelInstantiated | modelInitializationMode |
#define MASK_fmi2GetEventIndicators      (modelInitializationMode | modelEventMode | modelContinuousTimeMode | modelTerminated | modelError)
#define MASK_fmi2GetContinuousStates     MASK_fmi2GetEventIndicators
#define MASK_fmi2GetDerivatives          (modelEventMode | modelContinuousTimeMode | modelTerminated | modelError)
#define MASK_fmi2GetNominalsOfContinuousStates ( modelInstantiated | modelEventMode | modelContinuousTimeMode | modelTerminated | modelError)

// ---------------------------------------------------------------------------
// Function calls allowed state masks for Co-simulation
// ---------------------------------------------------------------------------
#define MASK_fmi2SetRealInputDerivatives (modelInstantiated | modelInitializationMode | modelStepComplete)
#define MASK_fmi2GetRealOutputDerivatives (modelStepComplete | modelStepFailed | modelStepCanceled | modelTerminated | modelError)
#define MASK_fmi2DoStep                  modelStepComplete
#define MASK_fmi2CancelStep              modelStepInProgress
#define MASK_fmi2GetStatus               (modelStepComplete | modelStepInProgress | modelStepFailed | modelTerminated)
#define MASK_fmi2GetRealStatus           MASK_fmi2GetStatus
#define MASK_fmi2GetIntegerStatus        MASK_fmi2GetStatus
#define MASK_fmi2GetBooleanStatus        MASK_fmi2GetStatus
#define MASK_fmi2GetStringStatus         MASK_fmi2GetStatus

#ifdef __cplusplus
} // closing brace for extern "C"
#endif
'''

###############################################################################
# fmi2Template.c
###############################################################################
fmi2Template_c = r'''#ifdef __cplusplus
extern "C"
#endif

///////////////////////////////////////////////////////////////////////////////
// FMI functions (common)
///////////////////////////////////////////////////////////////////////////////
fmi2Component fmi2Instantiate(fmi2String instanceName, fmi2Type fmuType, fmi2String fmuGUID,
                            fmi2String fmuResourceLocation, const fmi2CallbackFunctions *functions,
                            fmi2Boolean visible, fmi2Boolean loggingOn) {
    // Make a reference to the global instance
    ModelInstance *comp = &instance;

    // Logger is required
    if (!functions->logger) {
        return NULL;
    }

    // InstanceName is require
    if (!instanceName || strlen(instanceName) == 0) {
        functions->logger(functions->componentEnvironment, "?", fmi2Error, "error",
                "fmi2Instantiate: Missing instance name.");
        return NULL;
    }

    // fmuGUID required
    if (!fmuGUID || strlen(fmuGUID) == 0) {
        functions->logger(functions->componentEnvironment, instanceName, fmi2Error, "error",
                "fmi2Instantiate: Missing GUID.");
        return NULL;
    }

    // Compare GUID
    if (strcmp(fmuGUID, MODEL_GUID)) {
        functions->logger(functions->componentEnvironment, instanceName, fmi2Error, "error",
                "fmi2Instantiate: Wrong GUID %s. Expected %s.", fmuGUID, MODEL_GUID);
        return NULL;
    }

    // Default 
    if (loggingOn){
        int i = 0;
        for (i = 0; i < NUMBER_OF_CATEGORIES; i++) {
            comp->logCategories[i] = loggingOn;
        }
    }
    
    comp->time = 0; // overwrite in fmi2SetupExperiment, fmi2SetTime
    strcpy((char *)comp->instanceName, (char *)instanceName);
    comp->type = fmuType;
    comp->functions = functions;
    comp->componentEnvironment = functions->componentEnvironment;
    comp->loggingOn = loggingOn;
    comp->state = modelInstantiated;

    // Reset x to x0, u to u0
#if NX > 0
    resetX(comp);
    updateDerivatives(comp);
#endif
#if NU > 0
    resetU(comp);
    updateOutputs(comp);
#endif     

    // Log func call
    FILTERED_LOG(comp, fmi2OK, LOG_FMI_CALL, "fmi2Instantiate: GUID=%s", fmuGUID)
    
    return comp;
}


fmi2Status fmi2SetupExperiment(fmi2Component c, fmi2Boolean toleranceDefined, fmi2Real tolerance,
                            fmi2Real startTime, fmi2Boolean stopTimeDefined, fmi2Real stopTime) 
{
    ModelInstance *comp = (ModelInstance *)c;
    if (isInvalidState(comp, "fmi2SetupExperiment", MASK_fmi2SetupExperiment))
        return fmi2Error;
    FILTERED_LOG(comp, fmi2OK, LOG_FMI_CALL, "fmi2SetupExperiment: toleranceDefined=%d tolerance=%g",
        toleranceDefined, tolerance)
    comp->time = startTime;
    return fmi2OK;
}

fmi2Status fmi2EnterInitializationMode(fmi2Component c) {
    ModelInstance *comp = (ModelInstance *)c;
    if (isInvalidState(comp, "fmi2EnterInitializationMode", MASK_fmi2EnterInitializationMode))
        return fmi2Error;
    FILTERED_LOG(comp, fmi2OK, LOG_FMI_CALL, "fmi2EnterInitializationMode")

    comp->state = modelInitializationMode;
    return fmi2OK;
}

fmi2Status fmi2ExitInitializationMode(fmi2Component c) {
    ModelInstance *comp = (ModelInstance *)c;
    if (isInvalidState(comp, "fmi2ExitInitializationMode", MASK_fmi2ExitInitializationMode))
        return fmi2Error;
    FILTERED_LOG(comp, fmi2OK, LOG_FMI_CALL, "fmi2ExitInitializationMode")

    // if values were set and no fmi2GetXXX triggered update before,
    // ensure calculated values are updated now
    if (comp->isDirtyValues) {
#if NX > 0
        copyX0toX(comp);
#endif
#if NU > 0
        copyU0toU(comp);
#endif
#if NX > 0
        updateDerivatives(comp);
#endif
#if NY > 0
        updateOutputs(comp);
#endif
        comp->isDirtyValues = fmi2False;
    }

    if (comp->type == fmi2ModelExchange) {
        comp->state = modelEventMode;
    } else {
        comp->state = modelStepComplete;
    }
    return fmi2OK;
}

fmi2Status fmi2Terminate(fmi2Component c) {
    ModelInstance *comp = (ModelInstance *)c;
    if (isInvalidState(comp, "fmi2Terminate", MASK_fmi2Terminate))
        return fmi2Error;
    FILTERED_LOG(comp, fmi2OK, LOG_FMI_CALL, "fmi2Terminate")

    comp->state = modelTerminated;
    return fmi2OK;
}

fmi2Status fmi2Reset(fmi2Component c) {
    ModelInstance* comp = (ModelInstance *)c;
    if (isInvalidState(comp, "fmi2Reset", MASK_fmi2Reset))
        return fmi2Error;
    FILTERED_LOG(comp, fmi2OK, LOG_FMI_CALL, "fmi2Reset")

    comp->state = modelInstantiated;
#if NX > 0
    resetX(comp);
#endif
#if NU > 0
    resetU(comp);
#endif
    comp->isDirtyValues = fmi2True; // because we just called setStartValues
    return fmi2OK;
}

void fmi2FreeInstance(fmi2Component c) {
    ModelInstance *comp = (ModelInstance *)c;
    if (!comp) return;
    if (isInvalidState(comp, "fmi2FreeInstance", MASK_fmi2FreeInstance))
        return;
    FILTERED_LOG(comp, fmi2OK, LOG_FMI_CALL, "fmi2FreeInstance")
}


// ---------------------------------------------------------------------------
// FMI functions: class methods not depending of a specific model instance
// ---------------------------------------------------------------------------

const char* fmi2GetVersion() {
    return fmi2Version;
}

const char* fmi2GetTypesPlatform() {
    return fmi2TypesPlatform;
}

// ---------------------------------------------------------------------------
// FMI functions: logging control, setters and getters for Real, Integer,
// Boolean, String
// ---------------------------------------------------------------------------
fmi2Status fmi2SetDebugLogging(fmi2Component c, fmi2Boolean loggingOn, size_t nCategories, const fmi2String categories[]) {
    int i, j;
    ModelInstance *comp = (ModelInstance *)c;
    if (isInvalidState(comp, "fmi2SetDebugLogging", MASK_fmi2SetDebugLogging))
        return fmi2Error;
    comp->loggingOn = loggingOn;
    FILTERED_LOG(comp, fmi2OK, LOG_FMI_CALL, "fmi2SetDebugLogging")

    // reset all categories
    for (j = 0; j < NUMBER_OF_CATEGORIES; j++) {
        comp->logCategories[j] = fmi2False;
    }

    if (nCategories == 0) {
        // no category specified, set all categories to have loggingOn value
        for (j = 0; j < NUMBER_OF_CATEGORIES; j++) {
            comp->logCategories[j] = loggingOn;
        }
    } else {
        // set specific categories on
        for (i = 0; i < nCategories; i++) {
            fmi2Boolean categoryFound = fmi2False;
            for (j = 0; j < NUMBER_OF_CATEGORIES; j++) {
                if (strcmp(logCategoriesNames[j], categories[i]) == 0) {
                    comp->logCategories[j] = loggingOn;
                    categoryFound = fmi2True;
                    break;
                }
            }
            if (!categoryFound) {
                comp->functions->logger(comp->componentEnvironment, comp->instanceName, fmi2Warning,
                    logCategoriesNames[LOG_ERROR],
                    "logging category '%s' is not supported by model", categories[i]);
            }
        }
    }
    return fmi2OK;
}

fmi2Status fmi2GetReal(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, fmi2Real value[]) {
    int i;
    ModelInstance *comp = (ModelInstance *)c;
    
    if (isInvalidState(comp, "fmi2GetReal", MASK_fmi2GetReal))
        return fmi2Error;

    if (nvr > 0 && isNullPtr(comp, "fmi2GetReal", "vr[]", vr))
        return fmi2Error;

    if (nvr > 0 && isNullPtr(comp, "fmi2GetReal", "value[]", value))
        return fmi2Error;

    if (nvr > 0 && comp->isDirtyValues) {
        evaluate(comp);
        comp->isDirtyValues = fmi2False;
    }

    for (i = 0; i < nvr; i++) {
        if (isVROutOfRange(comp, "fmi2GetReal", vr[i], NR))
            return fmi2Error;
        value[i] = comp->r[vr[i]];
        FILTERED_LOG(comp, fmi2OK, LOG_FMI_CALL, "fmi2GetReal: #r%u# = %.16g", vr[i], value[i])
    }

    return fmi2OK;
}

fmi2Status fmi2GetInteger(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, fmi2Integer value[]) {
    ModelInstance *comp = (ModelInstance *)c;
    if (isInvalidState(comp, "fmi2GetInteger", MASK_fmi2GetInteger))
        return fmi2Error;
    
    // nvr must be zero
    if (nvr != 0) {
        return fmi2Error;
    }
    // vr and value must be null
    if (fmi2False != isNullPtr(comp, "fmi2GetInteger", "vr[]", vr) || fmi2False != isNullPtr(comp, "fmi2GetInteger", "value[]", value)){
        return fmi2Error;
    }
    return fmi2OK;    
}

fmi2Status fmi2GetBoolean(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, fmi2Boolean value[]) {
    ModelInstance *comp = (ModelInstance *)c;
    if (isInvalidState(comp, "fmi2GetBoolean", MASK_fmi2GetBoolean))
        return fmi2Error;
    
    // nvr must be zero
    if (nvr != 0) {
        return fmi2Error;
    }
    // vr and value must be null
    if (fmi2False != isNullPtr(comp, "fmi2GetBoolean", "vr[]", vr) || fmi2False != isNullPtr(comp, "fmi2GetBoolean", "value[]", value)){
        return fmi2Error;
    }
    return fmi2OK;    
}

fmi2Status fmi2GetString(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, fmi2String value[]) {
    ModelInstance *comp = (ModelInstance *)c;
    if (isInvalidState(comp, "fmi2GetString", MASK_fmi2GetString))
        return fmi2Error;
    
    // nvr must be zero
    if (nvr != 0) {
        return fmi2Error;
    }
    // vr and value must be null
    if (fmi2False != isNullPtr(comp, "fmi2GetString", "vr[]", vr) || fmi2False != isNullPtr(comp, "fmi2GetString", "value[]", value)){
        return fmi2Error;
    }
    return fmi2OK;
}

fmi2Status fmi2SetReal(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, const fmi2Real value[]) {
    int i;
    ModelInstance *comp = (ModelInstance *)c;
    if (isInvalidState(comp, "fmi2SetReal", MASK_fmi2SetReal))
        return fmi2Error;
    if (nvr > 0 && isNullPtr(comp, "fmi2SetReal", "vr[]", vr))
        return fmi2Error;
    if (nvr > 0 && isNullPtr(comp, "fmi2SetReal", "value[]", value))
        return fmi2Error;
    FILTERED_LOG(comp, fmi2OK, LOG_FMI_CALL, "fmi2SetReal: nvr = %d", nvr)

    for (i = 0; i < nvr; i++) {
        if (isVROutOfRange(comp, "fmi2SetReal", vr[i], NR))
            return fmi2Error;
        FILTERED_LOG(comp, fmi2OK, LOG_FMI_CALL, "fmi2SetReal: #r%d# = %.16g", vr[i], value[i])
        comp->r[vr[i]] = value[i];
    }
    if (nvr > 0) {
        comp->isDirtyValues = fmi2True;
    }
    return fmi2OK;
}

fmi2Status fmi2SetInteger(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, const fmi2Integer value[]) {
    ModelInstance *comp = (ModelInstance *)c;
    if (isInvalidState(comp, "fmi2SetInteger", MASK_fmi2SetInteger))
        return fmi2Error;

    // nvr must be zero
    if (nvr != 0) {
        return fmi2Error;
    }

    // vr and value must be null
    if (fmi2False != isNullPtr(comp, "fmi2SetInteger", "vr[]", vr) || fmi2False != isNullPtr(comp, "fmi2SetInteger", "value[]", value)){
        return fmi2Error;
    }

    return fmi2OK;
}

fmi2Status fmi2SetBoolean(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, const fmi2Boolean value[]) {
    ModelInstance *comp = (ModelInstance *)c;
    if (isInvalidState(comp, "fmi2SetBoolean", MASK_fmi2SetBoolean))
        return fmi2Error;

    // nvr must be zero
    if (nvr != 0) {
        return fmi2Error;
    }

    // vr and value must be null
    if (fmi2False != isNullPtr(comp, "fmi2SetBoolean", "vr[]", vr) || fmi2False != isNullPtr(comp, "fmi2SetBoolean", "value[]", value)){
        return fmi2Error;
    }

    return fmi2OK;
}

fmi2Status fmi2SetString (fmi2Component c, const fmi2ValueReference vr[], size_t nvr, const fmi2String value[]) {
    ModelInstance *comp = (ModelInstance *)c;
    if (isInvalidState(comp, "fmi2SetString", MASK_fmi2SetString))
        return fmi2Error;

    // nvr must be zero
    if (nvr != 0) {
        return fmi2Error;
    }

    // vr and value must be null
    if (fmi2False != isNullPtr(comp, "fmi2SetString", "vr[]", vr) || fmi2False != isNullPtr(comp, "fmi2SetString", "value[]", value)){
        return fmi2Error;
    }

    return fmi2OK;
}

fmi2Status fmi2GetFMUstate (fmi2Component c, fmi2FMUstate* FMUstate) {
    return unsupportedFunction(c, "fmi2GetFMUstate", MASK_fmi2GetFMUstate);
}
fmi2Status fmi2SetFMUstate (fmi2Component c, fmi2FMUstate FMUstate) {
    return unsupportedFunction(c, "fmi2SetFMUstate", MASK_fmi2SetFMUstate);
}
fmi2Status fmi2FreeFMUstate(fmi2Component c, fmi2FMUstate* FMUstate) {
    return unsupportedFunction(c, "fmi2FreeFMUstate", MASK_fmi2FreeFMUstate);
}
fmi2Status fmi2SerializedFMUstateSize(fmi2Component c, fmi2FMUstate FMUstate, size_t *size) {
    return unsupportedFunction(c, "fmi2SerializedFMUstateSize", MASK_fmi2SerializedFMUstateSize);
}
fmi2Status fmi2SerializeFMUstate (fmi2Component c, fmi2FMUstate FMUstate, fmi2Byte serializedState[], size_t size) {
    return unsupportedFunction(c, "fmi2SerializeFMUstate", MASK_fmi2SerializeFMUstate);
}
fmi2Status fmi2DeSerializeFMUstate (fmi2Component c, const fmi2Byte serializedState[], size_t size,
                                    fmi2FMUstate* FMUstate) {
    return unsupportedFunction(c, "fmi2DeSerializeFMUstate", MASK_fmi2DeSerializeFMUstate);
}

fmi2Status fmi2GetDirectionalDerivative(fmi2Component c, const fmi2ValueReference vUnknown_ref[], size_t nUnknown,
                                        const fmi2ValueReference vKnown_ref[] , size_t nKnown,
                                        const fmi2Real dvKnown[], fmi2Real dvUnknown[]) {
    return unsupportedFunction(c, "fmi2GetDirectionalDerivative", MASK_fmi2GetDirectionalDerivative);
}

// ---------------------------------------------------------------------------
// Functions for FMI for Co-Simulation
// ---------------------------------------------------------------------------
/* Simulating the slave */
fmi2Status fmi2SetRealInputDerivatives(fmi2Component c, const fmi2ValueReference vr[], size_t nvr,
                                     const fmi2Integer order[], const fmi2Real value[]) {
    ModelInstance *comp = (ModelInstance *)c;
    if (isInvalidState(comp, "fmi2SetRealInputDerivatives", MASK_fmi2SetRealInputDerivatives)) {
        return fmi2Error;
    }
    FILTERED_LOG(comp, fmi2OK, LOG_FMI_CALL, "fmi2SetRealInputDerivatives: nvr= %d", nvr)
    FILTERED_LOG(comp, fmi2Error, LOG_ERROR, "fmi2SetRealInputDerivatives: ignoring function call."
        " This model cannot interpolate inputs: canInterpolateInputs=\"fmi2False\"")
    return fmi2Error;
}

fmi2Status fmi2GetRealOutputDerivatives(fmi2Component c, const fmi2ValueReference vr[], size_t nvr,
                                      const fmi2Integer order[], fmi2Real value[]) {
    int i;
    ModelInstance *comp = (ModelInstance *)c;
    if (isInvalidState(comp, "fmi2GetRealOutputDerivatives", MASK_fmi2GetRealOutputDerivatives))
        return fmi2Error;
    FILTERED_LOG(comp, fmi2OK, LOG_FMI_CALL, "fmi2GetRealOutputDerivatives: nvr= %d", nvr)
    FILTERED_LOG(comp, fmi2Error, LOG_ERROR,"fmi2GetRealOutputDerivatives: ignoring function call."
        " This model cannot compute derivatives of outputs: MaxOutputDerivativeOrder=\"0\"")
    for (i = 0; i < nvr; i++) value[i] = 0;
    return fmi2Error;
}

fmi2Status fmi2CancelStep(fmi2Component c) {
    ModelInstance *comp = (ModelInstance *)c;
    if (isInvalidState(comp, "fmi2CancelStep", MASK_fmi2CancelStep)) {
        // always fmi2CancelStep is invalid, because model is never in modelStepInProgress state.
        return fmi2Error;
    }
    FILTERED_LOG(comp, fmi2OK, LOG_FMI_CALL, "fmi2CancelStep")
    FILTERED_LOG(comp, fmi2Error, LOG_ERROR,"fmi2CancelStep: Can be called when fmi2DoStep returned fmi2Pending."
        " This is not the case.");
    // comp->state = modelStepCanceled;
    return fmi2Error;
}

fmi2Status fmi2DoStep(fmi2Component c, fmi2Real currentCommunicationPoint,
                    fmi2Real communicationStepSize, fmi2Boolean noSetFMUStatePriorToCurrentPoint) {
    ModelInstance *comp = (ModelInstance *)c;
    // TODO: Find btter stepsize by looking at the eigen value!
    int k;
    const int n = 100; // how many Euler steps to perform for one do step
    double h = communicationStepSize / n;

    if (isInvalidState(comp, "fmi2DoStep", MASK_fmi2DoStep))
        return fmi2Error;

    FILTERED_LOG(comp, fmi2OK, LOG_FMI_CALL, "fmi2DoStep: "
        "currentCommunicationPoint = %g, "
        "communicationStepSize = %g, "
        "noSetFMUStatePriorToCurrentPoint = fmi2%s",
        currentCommunicationPoint, communicationStepSize, noSetFMUStatePriorToCurrentPoint ? "True" : "False")

    if (communicationStepSize <= 0) {
        FILTERED_LOG(comp, fmi2Error, LOG_ERROR,
            "fmi2DoStep: communication step size must be > 0. Fount %g.", communicationStepSize)
        comp->state = modelError;
        return fmi2Error;
    }

    // break the step into n steps and do forward Euler.
    comp->time = currentCommunicationPoint;
    for (k = 0; k < n; k++) {
        comp->time += h;
#if NX > 0
        updateDerivatives(comp);
        updateStates(comp, h);
#endif
    }

    // Update outputs based on new state values
    updateOutputs(comp);
    return fmi2OK;
}

/* Inquire slave status */
static fmi2Status getStatus(char* fname, fmi2Component c, const fmi2StatusKind s) {
    const char *statusKind[3] = {"fmi2DoStepStatus","fmi2PendingStatus","fmi2LastSuccessfulTime"};
    ModelInstance *comp = (ModelInstance *)c;
    if (isInvalidState(comp, fname, MASK_fmi2GetStatus)) // all get status have the same MASK_fmi2GetStatus
            return fmi2Error;
    FILTERED_LOG(comp, fmi2OK, LOG_FMI_CALL, "$s: fmi2StatusKind = %s", fname, statusKind[s])

    switch(s) {
        case fmi2DoStepStatus: FILTERED_LOG(comp, fmi2Error, LOG_ERROR,
            "%s: Can be called with fmi2DoStepStatus when fmi2DoStep returned fmi2Pending."
            " This is not the case.", fname)
            break;
        case fmi2PendingStatus: FILTERED_LOG(comp, fmi2Error, LOG_ERROR,
            "%s: Can be called with fmi2PendingStatus when fmi2DoStep returned fmi2Pending."
            " This is not the case.", fname)
            break;
        case fmi2LastSuccessfulTime: FILTERED_LOG(comp, fmi2Error, LOG_ERROR,
            "%s: Can be called with fmi2LastSuccessfulTime when fmi2DoStep returned fmi2Discard."
            " This is not the case.", fname)
            break;
        case fmi2Terminated: FILTERED_LOG(comp, fmi2Error, LOG_ERROR,
            "%s: Can be called with fmi2Terminated when fmi2DoStep returned fmi2Discard."
            " This is not the case.", fname)
            break;
    }
    return fmi2Discard;
}

fmi2Status fmi2GetStatus(fmi2Component c, const fmi2StatusKind s, fmi2Status *value) {
    return getStatus("fmi2GetStatus", c, s);
}

fmi2Status fmi2GetRealStatus(fmi2Component c, const fmi2StatusKind s, fmi2Real *value) {
    if (s == fmi2LastSuccessfulTime) {
        ModelInstance *comp = (ModelInstance *)c;
        if (isInvalidState(comp, "fmi2GetRealStatus", MASK_fmi2GetRealStatus))
            return fmi2Error;
        *value = comp->time;
        return fmi2OK;
    }
    return getStatus("fmi2GetRealStatus", c, s);
}

fmi2Status fmi2GetIntegerStatus(fmi2Component c, const fmi2StatusKind s, fmi2Integer *value) {
    return getStatus("fmi2GetIntegerStatus", c, s);
}

fmi2Status fmi2GetBooleanStatus(fmi2Component c, const fmi2StatusKind s, fmi2Boolean *value) {
    if (s == fmi2Terminated) {
        ModelInstance *comp = (ModelInstance *)c;
        if (isInvalidState(comp, "fmi2GetBooleanStatus", MASK_fmi2GetBooleanStatus))
            return fmi2Error;
        return fmi2OK;
    }
    return getStatus("fmi2GetBooleanStatus", c, s);
}

fmi2Status fmi2GetStringStatus(fmi2Component c, const fmi2StatusKind s, fmi2String *value) {
    return getStatus("fmi2GetStringStatus", c, s);
}

// ---------------------------------------------------------------------------
// Functions for FMI2 for Model Exchange
// ---------------------------------------------------------------------------
/* Enter and exit the different modes */
fmi2Status fmi2EnterEventMode(fmi2Component c) {
    ModelInstance *comp = (ModelInstance *)c;
    if (isInvalidState(comp, "fmi2EnterEventMode", MASK_fmi2EnterEventMode))
        return fmi2Error;
    FILTERED_LOG(comp, fmi2OK, LOG_FMI_CALL, "fmi2EnterEventMode")

    comp->state = modelEventMode;
    return fmi2OK;
}

fmi2Status fmi2NewDiscreteStates(fmi2Component c, fmi2EventInfo *eventInfo) {
    ModelInstance *comp = (ModelInstance *)c;
    if (isInvalidState(comp, "fmi2NewDiscreteStates", MASK_fmi2NewDiscreteStates))
        return fmi2Error;
    FILTERED_LOG(comp, fmi2OK, LOG_FMI_CALL, "fmi2NewDiscreteStates")
    return fmi2OK;
}


fmi2Status fmi2EnterContinuousTimeMode(fmi2Component c) {
    ModelInstance *comp = (ModelInstance *)c;
    if (isInvalidState(comp, "fmi2EnterContinuousTimeMode", MASK_fmi2EnterContinuousTimeMode))
        return fmi2Error;
    FILTERED_LOG(comp, fmi2OK, LOG_FMI_CALL,"fmi2EnterContinuousTimeMode")

    comp->state = modelContinuousTimeMode;
    return fmi2OK;
}

fmi2Status fmi2CompletedIntegratorStep(fmi2Component c, fmi2Boolean noSetFMUStatePriorToCurrentPoint,
                                     fmi2Boolean *enterEventMode, fmi2Boolean *terminateSimulation) {
    ModelInstance *comp = (ModelInstance *)c;
    if (isInvalidState(comp, "fmi2CompletedIntegratorStep", MASK_fmi2CompletedIntegratorStep))
        return fmi2Error;
    if (isNullPtr(comp, "fmi2CompletedIntegratorStep", "enterEventMode", enterEventMode))
        return fmi2Error;
    if (isNullPtr(comp, "fmi2CompletedIntegratorStep", "terminateSimulation", terminateSimulation))
        return fmi2Error;
    FILTERED_LOG(comp, fmi2OK, LOG_FMI_CALL,"fmi2CompletedIntegratorStep")
    *enterEventMode = fmi2False;
    *terminateSimulation = fmi2False;
    return fmi2OK;
}

/* Providing independent variables and re-initialization of caching */
fmi2Status fmi2SetTime(fmi2Component c, fmi2Real time) {
    ModelInstance *comp = (ModelInstance *)c;
    if (isInvalidState(comp, "fmi2SetTime", MASK_fmi2SetTime))
        return fmi2Error;
    FILTERED_LOG(comp, fmi2OK, LOG_FMI_CALL, "fmi2SetTime: time=%.16g", time)
    comp->time = time;
    return fmi2OK;
}

fmi2Status fmi2SetContinuousStates(fmi2Component c, const fmi2Real x[], size_t nx){
    ModelInstance *comp = (ModelInstance *)c;
    int i;
    if (isInvalidState(comp, "fmi2SetContinuousStates", MASK_fmi2SetContinuousStates))
        return fmi2Error;
    if (isInvalidNumber(comp, "fmi2SetContinuousStates", "nx", nx, NX))
        return fmi2Error;
    if (isNullPtr(comp, "fmi2SetContinuousStates", "x[]", x))
        return fmi2Error;
#if NX > 0
    for (i = 0; i < nx; i++) {
        fmi2ValueReference vr = vrs_x[i];
        FILTERED_LOG(comp, fmi2OK, LOG_FMI_CALL, "fmi2SetContinuousStates: #r%d#=%.16g", vr, x[i])
        assert(vr < NR);
        comp->r[vr] = x[i];
    }
#endif
#if NY > 0
    updateOutputs(comp);
#endif
    return fmi2OK;
}

/* Evaluation of the model equations */
fmi2Status fmi2GetDerivatives(fmi2Component c, fmi2Real derivatives[], size_t nx) {
    int i;
    ModelInstance* comp = (ModelInstance *)c;
    if (isInvalidState(comp, "fmi2GetDerivatives", MASK_fmi2GetDerivatives))
        return fmi2Error;
    if (isInvalidNumber(comp, "fmi2GetDerivatives", "nx", nx, NX))
        return fmi2Error;
    if (isNullPtr(comp, "fmi2GetDerivatives", "derivatives[]", derivatives))
        return fmi2Error;
#if NX > 0
    updateDerivatives(comp);
    for (i = 0; i < NX; ++i){
        fmi2ValueReference der_i = vrs_der[i];
        derivatives[i] = comp->r[der_i];
        FILTERED_LOG(comp, fmi2OK, LOG_FMI_CALL, "fmi2GetDerivatives: #r%d# = %.16g", der_i, derivatives[i])
    }
#endif
    return fmi2OK;
}

fmi2Status fmi2GetEventIndicators(fmi2Component c, fmi2Real eventIndicators[], size_t ni) {
    ModelInstance *comp = (ModelInstance *)c;
    if (isInvalidState(comp, "fmi2GetEventIndicators", MASK_fmi2GetEventIndicators))
        return fmi2Error;
    if (isInvalidNumber(comp, "fmi2GetEventIndicators", "ni", ni, 0))
        return fmi2Error;

    return fmi2OK;
}

fmi2Status fmi2GetContinuousStates(fmi2Component c, fmi2Real states[], size_t nx) {
    int i;
    ModelInstance *comp = (ModelInstance *)c;
    if (isInvalidState(comp, "fmi2GetContinuousStates", MASK_fmi2GetContinuousStates))
        return fmi2Error;
    if (isInvalidNumber(comp, "fmi2GetContinuousStates", "nx", nx, NX))
        return fmi2Error;
    if (isNullPtr(comp, "fmi2GetContinuousStates", "states[]", states))
        return fmi2Error;
#if NX>0
    for (i = 0; i < nx; i++) {
        fmi2ValueReference vr = vrs_x[i];
        states[i] = comp->r[vr]; // to be implemented by the includer of this file
        FILTERED_LOG(comp, fmi2OK, LOG_FMI_CALL, "fmi2GetContinuousStates: #r%u# = %.16g", vr, states[i])
    }
#endif
    return fmi2OK;
}

fmi2Status fmi2GetNominalsOfContinuousStates(fmi2Component c, fmi2Real x_nominal[], size_t nx) {
    int i;
    ModelInstance *comp = (ModelInstance *)c;
    if (isInvalidState(comp, "fmi2GetNominalsOfContinuousStates", MASK_fmi2GetNominalsOfContinuousStates))
        return fmi2Error;
    if (isInvalidNumber(comp, "fmi2GetNominalContinuousStates", "nx", nx, NX))
        return fmi2Error;
    if (isNullPtr(comp, "fmi2GetNominalContinuousStates", "x_nominal[]", x_nominal))
        return fmi2Error;
    FILTERED_LOG(comp, fmi2OK, LOG_FMI_CALL, "fmi2GetNominalContinuousStates: x_nominal[0..%d] = 1.0", nx-1)
    for (i = 0; i < nx; i++)
        x_nominal[i] = 1;
    return fmi2OK;
}

#ifdef __cplusplus
}
#endif
'''

###############################################################################
# fmi2Functions.h
###############################################################################
fmi2Functions_h = r'''#ifndef fmi2Functions_h
#define fmi2Functions_h

/* This header file must be utilized when compiling a FMU.
   It defines all functions of the
         FMI 2.0.2 Model Exchange and Co-Simulation Interface.

   In order to have unique function names even if several FMUs
   are compiled together (e.g. for embedded systems), every "real" function name
   is constructed by prepending the function name by "FMI2_FUNCTION_PREFIX".
   Therefore, the typical usage is:

      #define FMI2_FUNCTION_PREFIX MyModel_
      #include "fmi2Functions.h"

   As a result, a function that is defined as "fmi2GetDerivatives" in this header file,
   is actually getting the name "MyModel_fmi2GetDerivatives".

   This only holds if the FMU is shipped in C source code, or is compiled in a
   static link library. For FMUs compiled in a DLL/sharedObject, the "actual" function
   names are used and "FMI2_FUNCTION_PREFIX" must not be defined.

   Revisions:
   - Sep. 29, 2019: License changed to 2-clause BSD License (without extensions)
   - Apr.  9, 2014: All prefixes "fmi" renamed to "fmi2" (decision from April 8)
   - Mar. 26, 2014: FMI_Export set to empty value if FMI_Export and FMI_FUNCTION_PREFIX
                    are not defined (#173)
   - Oct. 11, 2013: Functions of ModelExchange and CoSimulation merged:
                      fmiInstantiateModel , fmiInstantiateSlave  -> fmiInstantiate
                      fmiFreeModelInstance, fmiFreeSlaveInstance -> fmiFreeInstance
                      fmiEnterModelInitializationMode, fmiEnterSlaveInitializationMode -> fmiEnterInitializationMode
                      fmiExitModelInitializationMode , fmiExitSlaveInitializationMode  -> fmiExitInitializationMode
                      fmiTerminateModel, fmiTerminateSlave  -> fmiTerminate
                      fmiResetSlave -> fmiReset (now also for ModelExchange and not only for CoSimulation)
                    Functions renamed:
                      fmiUpdateDiscreteStates -> fmiNewDiscreteStates
   - June 13, 2013: Functions removed:
                       fmiInitializeModel
                       fmiEventUpdate
                       fmiCompletedEventIteration
                       fmiInitializeSlave
                    Functions added:
                       fmiEnterModelInitializationMode
                       fmiExitModelInitializationMode
                       fmiEnterEventMode
                       fmiUpdateDiscreteStates
                       fmiEnterContinuousTimeMode
                       fmiEnterSlaveInitializationMode;
                       fmiExitSlaveInitializationMode;
   - Feb. 17, 2013: Portability improvements:
                       o DllExport changed to FMI_Export
                       o FUNCTION_PREFIX changed to FMI_FUNCTION_PREFIX
                       o Allow undefined FMI_FUNCTION_PREFIX (meaning no prefix is used)
                    Changed function name "fmiTerminate" to "fmiTerminateModel" (due to #113)
                    Changed function name "fmiGetNominalContinuousState" to
                                          "fmiGetNominalsOfContinuousStates"
                    Removed fmiGetStateValueReferences.
   - Nov. 14, 2011: Adapted to FMI 2.0:
                       o Split into two files (fmiFunctions.h, fmiTypes.h) in order
                         that code that dynamically loads an FMU can directly
                         utilize the header files).
                       o Added C++ encapsulation of C-part, in order that the header
                         file can be directly utilized in C++ code.
                       o fmiCallbackFunctions is passed as pointer to fmiInstantiateXXX
                       o stepFinished within fmiCallbackFunctions has as first
                         argument "fmiComponentEnvironment" and not "fmiComponent".
                       o New functions to get and set the complete FMU state
                         and to compute partial derivatives.
   - Nov.  4, 2010: Adapted to specification text:
                       o fmiGetModelTypesPlatform renamed to fmiGetTypesPlatform
                       o fmiInstantiateSlave: Argument GUID     replaced by fmuGUID
                                              Argument mimetype replaced by mimeType
                       o tabs replaced by spaces
   - Oct. 16, 2010: Functions for FMI for Co-simulation added
   - Jan. 20, 2010: stateValueReferencesChanged added to struct fmiEventInfo (ticket #27)
                    (by M. Otter, DLR)
                    Added WIN32 pragma to define the struct layout (ticket #34)
                    (by J. Mauss, QTronic)
   - Jan.  4, 2010: Removed argument intermediateResults from fmiInitialize
                    Renamed macro fmiGetModelFunctionsVersion to fmiGetVersion
                    Renamed macro fmiModelFunctionsVersion to fmiVersion
                    Replaced fmiModel by fmiComponent in decl of fmiInstantiateModel
                    (by J. Mauss, QTronic)
   - Dec. 17, 2009: Changed extension "me" to "fmi" (by Martin Otter, DLR).
   - Dez. 14, 2009: Added eventInfo to meInitialize and added
                    meGetNominalContinuousStates (by Martin Otter, DLR)
   - Sept. 9, 2009: Added DllExport (according to Peter Nilsson's suggestion)
                    (by A. Junghanns, QTronic)
   - Sept. 9, 2009: Changes according to FMI-meeting on July 21:
                    meInquireModelTypesVersion     -> meGetModelTypesPlatform
                    meInquireModelFunctionsVersion -> meGetModelFunctionsVersion
                    meSetStates                    -> meSetContinuousStates
                    meGetStates                    -> meGetContinuousStates
                    removal of meInitializeModelClass
                    removal of meGetTime
                    change of arguments of meInstantiateModel
                    change of arguments of meCompletedIntegratorStep
                    (by Martin Otter, DLR):
   - July 19, 2009: Added "me" as prefix to file names (by Martin Otter, DLR).
   - March 2, 2009: Changed function definitions according to the last design
                    meeting with additional improvements (by Martin Otter, DLR).
   - Dec. 3 , 2008: First version by Martin Otter (DLR) and Hans Olsson (Dynasim).


   Copyright (C) 2008-2011 MODELISAR consortium,
                 2012-2020 Modelica Association Project "FMI"
                 All rights reserved.

   This file is licensed by the copyright holders under the 2-Clause BSD License
   (https://opensource.org/licenses/BSD-2-Clause):

   ----------------------------------------------------------------------------
   Redistribution and use in source and binary forms, with or without
   modification, are permitted provided that the following conditions are met:

   - Redistributions of source code must retain the above copyright notice,
     this list of conditions and the following disclaimer.

   - Redistributions in binary form must reproduce the above copyright notice,
     this list of conditions and the following disclaimer in the documentation
     and/or other materials provided with the distribution.

   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
   "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
   TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
   PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
   CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
   EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
   OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
   WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
   OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
   ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
   ----------------------------------------------------------------------------
*/

#ifdef __cplusplus
extern "C" {
#endif

#include "fmi2TypesPlatform.h"
#include "fmi2FunctionTypes.h"
#include <stdlib.h>


/*
  Export FMI2 API functions on Windows and under GCC.
  If custom linking is desired then the FMI2_Export must be
  defined before including this file. For instance,
  it may be set to __declspec(dllimport).
*/
#if !defined(FMI2_Export)
  #if !defined(FMI2_FUNCTION_PREFIX)
    #if defined _WIN32 || defined __CYGWIN__
     /* Note: both gcc & MSVC on Windows support this syntax. */
        #define FMI2_Export __declspec(dllexport)
    #else
      #if __GNUC__ >= 4
        #define FMI2_Export __attribute__ ((visibility ("default")))
      #else
        #define FMI2_Export
      #endif
    #endif
  #else
    #define FMI2_Export
  #endif
#endif

/* Macros to construct the real function name
   (prepend function name by FMI2_FUNCTION_PREFIX) */
#if defined(FMI2_FUNCTION_PREFIX)
  #define fmi2Paste(a,b)     a ## b
  #define fmi2PasteB(a,b)    fmi2Paste(a,b)
  #define fmi2FullName(name) fmi2PasteB(FMI2_FUNCTION_PREFIX, name)
#else
  #define fmi2FullName(name) name
#endif

/***************************************************
Common Functions
****************************************************/
#define fmi2GetTypesPlatform         fmi2FullName(fmi2GetTypesPlatform)
#define fmi2GetVersion               fmi2FullName(fmi2GetVersion)
#define fmi2SetDebugLogging          fmi2FullName(fmi2SetDebugLogging)
#define fmi2Instantiate              fmi2FullName(fmi2Instantiate)
#define fmi2FreeInstance             fmi2FullName(fmi2FreeInstance)
#define fmi2SetupExperiment          fmi2FullName(fmi2SetupExperiment)
#define fmi2EnterInitializationMode  fmi2FullName(fmi2EnterInitializationMode)
#define fmi2ExitInitializationMode   fmi2FullName(fmi2ExitInitializationMode)
#define fmi2Terminate                fmi2FullName(fmi2Terminate)
#define fmi2Reset                    fmi2FullName(fmi2Reset)
#define fmi2GetReal                  fmi2FullName(fmi2GetReal)
#define fmi2GetInteger               fmi2FullName(fmi2GetInteger)
#define fmi2GetBoolean               fmi2FullName(fmi2GetBoolean)
#define fmi2GetString                fmi2FullName(fmi2GetString)
#define fmi2SetReal                  fmi2FullName(fmi2SetReal)
#define fmi2SetInteger               fmi2FullName(fmi2SetInteger)
#define fmi2SetBoolean               fmi2FullName(fmi2SetBoolean)
#define fmi2SetString                fmi2FullName(fmi2SetString)
#define fmi2GetFMUstate              fmi2FullName(fmi2GetFMUstate)
#define fmi2SetFMUstate              fmi2FullName(fmi2SetFMUstate)
#define fmi2FreeFMUstate             fmi2FullName(fmi2FreeFMUstate)
#define fmi2SerializedFMUstateSize   fmi2FullName(fmi2SerializedFMUstateSize)
#define fmi2SerializeFMUstate        fmi2FullName(fmi2SerializeFMUstate)
#define fmi2DeSerializeFMUstate      fmi2FullName(fmi2DeSerializeFMUstate)
#define fmi2GetDirectionalDerivative fmi2FullName(fmi2GetDirectionalDerivative)


/***************************************************
Functions for FMI2 for Model Exchange
****************************************************/
#define fmi2EnterEventMode                fmi2FullName(fmi2EnterEventMode)
#define fmi2NewDiscreteStates             fmi2FullName(fmi2NewDiscreteStates)
#define fmi2EnterContinuousTimeMode       fmi2FullName(fmi2EnterContinuousTimeMode)
#define fmi2CompletedIntegratorStep       fmi2FullName(fmi2CompletedIntegratorStep)
#define fmi2SetTime                       fmi2FullName(fmi2SetTime)
#define fmi2SetContinuousStates           fmi2FullName(fmi2SetContinuousStates)
#define fmi2GetDerivatives                fmi2FullName(fmi2GetDerivatives)
#define fmi2GetEventIndicators            fmi2FullName(fmi2GetEventIndicators)
#define fmi2GetContinuousStates           fmi2FullName(fmi2GetContinuousStates)
#define fmi2GetNominalsOfContinuousStates fmi2FullName(fmi2GetNominalsOfContinuousStates)


/***************************************************
Functions for FMI2 for Co-Simulation
****************************************************/
#define fmi2SetRealInputDerivatives      fmi2FullName(fmi2SetRealInputDerivatives)
#define fmi2GetRealOutputDerivatives     fmi2FullName(fmi2GetRealOutputDerivatives)
#define fmi2DoStep                       fmi2FullName(fmi2DoStep)
#define fmi2CancelStep                   fmi2FullName(fmi2CancelStep)
#define fmi2GetStatus                    fmi2FullName(fmi2GetStatus)
#define fmi2GetRealStatus                fmi2FullName(fmi2GetRealStatus)
#define fmi2GetIntegerStatus             fmi2FullName(fmi2GetIntegerStatus)
#define fmi2GetBooleanStatus             fmi2FullName(fmi2GetBooleanStatus)
#define fmi2GetStringStatus              fmi2FullName(fmi2GetStringStatus)

/* Version number */
#define fmi2Version "2.0"


/***************************************************
Common Functions
****************************************************/

/* Inquire version numbers of header files */
   FMI2_Export fmi2GetTypesPlatformTYPE fmi2GetTypesPlatform;
   FMI2_Export fmi2GetVersionTYPE       fmi2GetVersion;
   FMI2_Export fmi2SetDebugLoggingTYPE  fmi2SetDebugLogging;

/* Creation and destruction of FMU instances */
   FMI2_Export fmi2InstantiateTYPE  fmi2Instantiate;
   FMI2_Export fmi2FreeInstanceTYPE fmi2FreeInstance;

/* Enter and exit initialization mode, terminate and reset */
   FMI2_Export fmi2SetupExperimentTYPE         fmi2SetupExperiment;
   FMI2_Export fmi2EnterInitializationModeTYPE fmi2EnterInitializationMode;
   FMI2_Export fmi2ExitInitializationModeTYPE  fmi2ExitInitializationMode;
   FMI2_Export fmi2TerminateTYPE               fmi2Terminate;
   FMI2_Export fmi2ResetTYPE                   fmi2Reset;

/* Getting and setting variables values */
   FMI2_Export fmi2GetRealTYPE    fmi2GetReal;
   FMI2_Export fmi2GetIntegerTYPE fmi2GetInteger;
   FMI2_Export fmi2GetBooleanTYPE fmi2GetBoolean;
   FMI2_Export fmi2GetStringTYPE  fmi2GetString;

   FMI2_Export fmi2SetRealTYPE    fmi2SetReal;
   FMI2_Export fmi2SetIntegerTYPE fmi2SetInteger;
   FMI2_Export fmi2SetBooleanTYPE fmi2SetBoolean;
   FMI2_Export fmi2SetStringTYPE  fmi2SetString;

/* Getting and setting the internal FMU state */
   FMI2_Export fmi2GetFMUstateTYPE            fmi2GetFMUstate;
   FMI2_Export fmi2SetFMUstateTYPE            fmi2SetFMUstate;
   FMI2_Export fmi2FreeFMUstateTYPE           fmi2FreeFMUstate;
   FMI2_Export fmi2SerializedFMUstateSizeTYPE fmi2SerializedFMUstateSize;
   FMI2_Export fmi2SerializeFMUstateTYPE      fmi2SerializeFMUstate;
   FMI2_Export fmi2DeSerializeFMUstateTYPE    fmi2DeSerializeFMUstate;

/* Getting partial derivatives */
   FMI2_Export fmi2GetDirectionalDerivativeTYPE fmi2GetDirectionalDerivative;


/***************************************************
Functions for FMI2 for Model Exchange
****************************************************/

/* Enter and exit the different modes */
   FMI2_Export fmi2EnterEventModeTYPE               fmi2EnterEventMode;
   FMI2_Export fmi2NewDiscreteStatesTYPE            fmi2NewDiscreteStates;
   FMI2_Export fmi2EnterContinuousTimeModeTYPE      fmi2EnterContinuousTimeMode;
   FMI2_Export fmi2CompletedIntegratorStepTYPE      fmi2CompletedIntegratorStep;

/* Providing independent variables and re-initialization of caching */
   FMI2_Export fmi2SetTimeTYPE             fmi2SetTime;
   FMI2_Export fmi2SetContinuousStatesTYPE fmi2SetContinuousStates;

/* Evaluation of the model equations */
   FMI2_Export fmi2GetDerivativesTYPE                fmi2GetDerivatives;
   FMI2_Export fmi2GetEventIndicatorsTYPE            fmi2GetEventIndicators;
   FMI2_Export fmi2GetContinuousStatesTYPE           fmi2GetContinuousStates;
   FMI2_Export fmi2GetNominalsOfContinuousStatesTYPE fmi2GetNominalsOfContinuousStates;


/***************************************************
Functions for FMI2 for Co-Simulation
****************************************************/

/* Simulating the slave */
   FMI2_Export fmi2SetRealInputDerivativesTYPE  fmi2SetRealInputDerivatives;
   FMI2_Export fmi2GetRealOutputDerivativesTYPE fmi2GetRealOutputDerivatives;

   FMI2_Export fmi2DoStepTYPE     fmi2DoStep;
   FMI2_Export fmi2CancelStepTYPE fmi2CancelStep;

/* Inquire slave status */
   FMI2_Export fmi2GetStatusTYPE        fmi2GetStatus;
   FMI2_Export fmi2GetRealStatusTYPE    fmi2GetRealStatus;
   FMI2_Export fmi2GetIntegerStatusTYPE fmi2GetIntegerStatus;
   FMI2_Export fmi2GetBooleanStatusTYPE fmi2GetBooleanStatus;
   FMI2_Export fmi2GetStringStatusTYPE  fmi2GetStringStatus;

#ifdef __cplusplus
}  /* end of extern "C" { */
#endif

#endif /* fmi2Functions_h */
'''

###############################################################################
# fmi2FunctionTypes.h
###############################################################################
fmi2FunctionTypes_h = r'''#ifndef fmi2FunctionTypes_h
#define fmi2FunctionTypes_h

#include "fmi2TypesPlatform.h"

/* This header file must be utilized when compiling an FMU or an FMI master.
   It declares data and function types for FMI 2.0.2

   Revisions:
   - Sep. 30, 2019: License changed to 2-clause BSD License (without extensions)
   - Jul.  5, 2019: Remove const modifier from fields of fmi2CallbackFunctions  (#216)
   - Sep.  6, 2018: Parameter names added to function prototypes
   - Apr.  9, 2014: all prefixes "fmi" renamed to "fmi2" (decision from April 8)
   - Apr.  3, 2014: Added #include <stddef.h> for size_t definition
   - Mar. 27, 2014: Added #include "fmiTypesPlatform.h" (#179)
   - Mar. 26, 2014: Introduced function argument "void" for the functions (#171)
                      fmiGetTypesPlatformTYPE and fmiGetVersionTYPE
   - Oct. 11, 2013: Functions of ModelExchange and CoSimulation merged:
                      fmiInstantiateModelTYPE , fmiInstantiateSlaveTYPE  -> fmiInstantiateTYPE
                      fmiFreeModelInstanceTYPE, fmiFreeSlaveInstanceTYPE -> fmiFreeInstanceTYPE
                      fmiEnterModelInitializationModeTYPE, fmiEnterSlaveInitializationModeTYPE -> fmiEnterInitializationModeTYPE
                      fmiExitModelInitializationModeTYPE , fmiExitSlaveInitializationModeTYPE  -> fmiExitInitializationModeTYPE
                      fmiTerminateModelTYPE , fmiTerminateSlaveTYPE  -> fmiTerminate
                      fmiResetSlave -> fmiReset (now also for ModelExchange and not only for CoSimulation)
                    Functions renamed
                      fmiUpdateDiscreteStatesTYPE -> fmiNewDiscreteStatesTYPE
                    Renamed elements of the enumeration fmiEventInfo
                      upcomingTimeEvent             -> nextEventTimeDefined // due to generic naming scheme: varDefined + var
                      newUpdateDiscreteStatesNeeded -> newDiscreteStatesNeeded;
   - June 13, 2013: Changed type fmiEventInfo
                    Functions removed:
                       fmiInitializeModelTYPE
                       fmiEventUpdateTYPE
                       fmiCompletedEventIterationTYPE
                       fmiInitializeSlaveTYPE
                    Functions added:
                       fmiEnterModelInitializationModeTYPE
                       fmiExitModelInitializationModeTYPE
                       fmiEnterEventModeTYPE
                       fmiUpdateDiscreteStatesTYPE
                       fmiEnterContinuousTimeModeTYPE
                       fmiEnterSlaveInitializationModeTYPE;
                       fmiExitSlaveInitializationModeTYPE;
   - Feb. 17, 2013: Added third argument to fmiCompletedIntegratorStepTYPE
                    Changed function name "fmiTerminateType" to "fmiTerminateModelType" (due to #113)
                    Changed function name "fmiGetNominalContinuousStateTYPE" to
                                          "fmiGetNominalsOfContinuousStatesTYPE"
                    Removed fmiGetStateValueReferencesTYPE.
   - Nov. 14, 2011: First public Version


   Copyright (C) 2008-2011 MODELISAR consortium,
                 2012-2020 Modelica Association Project "FMI"
                 All rights reserved.

   This file is licensed by the copyright holders under the 2-Clause BSD License
   (https://opensource.org/licenses/BSD-2-Clause):

   ----------------------------------------------------------------------------
   Redistribution and use in source and binary forms, with or without
   modification, are permitted provided that the following conditions are met:

   - Redistributions of source code must retain the above copyright notice,
     this list of conditions and the following disclaimer.

   - Redistributions in binary form must reproduce the above copyright notice,
     this list of conditions and the following disclaimer in the documentation
     and/or other materials provided with the distribution.

   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
   "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
   TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
   PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
   CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
   EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
   OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
   WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
   OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
   ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
   ----------------------------------------------------------------------------
*/

#ifdef __cplusplus
extern "C" {
#endif

/* make sure all compiler use the same alignment policies for structures */
#if defined _MSC_VER || defined __GNUC__
#pragma pack(push,8)
#endif

/* Include stddef.h, in order that size_t etc. is defined */
#include <stddef.h>


/* Type definitions */
typedef enum {
    fmi2OK,
    fmi2Warning,
    fmi2Discard,
    fmi2Error,
    fmi2Fatal,
    fmi2Pending
} fmi2Status;

typedef enum {
    fmi2ModelExchange,
    fmi2CoSimulation
} fmi2Type;

typedef enum {
    fmi2DoStepStatus,
    fmi2PendingStatus,
    fmi2LastSuccessfulTime,
    fmi2Terminated
} fmi2StatusKind;

typedef void      (*fmi2CallbackLogger)        (fmi2ComponentEnvironment componentEnvironment,
                                                fmi2String instanceName,
                                                fmi2Status status,
                                                fmi2String category,
                                                fmi2String message,
                                                ...);
typedef void*     (*fmi2CallbackAllocateMemory)(size_t nobj, size_t size);
typedef void      (*fmi2CallbackFreeMemory)    (void* obj);
typedef void      (*fmi2StepFinished)          (fmi2ComponentEnvironment componentEnvironment,
                                                fmi2Status status);

typedef struct {
   fmi2CallbackLogger         logger;
   fmi2CallbackAllocateMemory allocateMemory;
   fmi2CallbackFreeMemory     freeMemory;
   fmi2StepFinished           stepFinished;
   fmi2ComponentEnvironment   componentEnvironment;
} fmi2CallbackFunctions;

typedef struct {
   fmi2Boolean newDiscreteStatesNeeded;
   fmi2Boolean terminateSimulation;
   fmi2Boolean nominalsOfContinuousStatesChanged;
   fmi2Boolean valuesOfContinuousStatesChanged;
   fmi2Boolean nextEventTimeDefined;
   fmi2Real    nextEventTime;
} fmi2EventInfo;


/* reset alignment policy to the one set before reading this file */
#if defined _MSC_VER || defined __GNUC__
#pragma pack(pop)
#endif


/* Define fmi2 function pointer types to simplify dynamic loading */

/***************************************************
Types for Common Functions
****************************************************/

/* Inquire version numbers of header files and setting logging status */
    typedef const char* fmi2GetTypesPlatformTYPE(void);
    typedef const char* fmi2GetVersionTYPE(void);
    typedef fmi2Status  fmi2SetDebugLoggingTYPE(fmi2Component c,
                                                fmi2Boolean loggingOn,
                                                size_t nCategories,
                                                const fmi2String categories[]);

/* Creation and destruction of FMU instances and setting debug status */
    typedef fmi2Component fmi2InstantiateTYPE(fmi2String instanceName,
                                              fmi2Type fmuType,
                                              fmi2String fmuGUID,
                                              fmi2String fmuResourceLocation,
                                              const fmi2CallbackFunctions* functions,
                                              fmi2Boolean visible,
                                              fmi2Boolean loggingOn);
   typedef void          fmi2FreeInstanceTYPE(fmi2Component c);

/* Enter and exit initialization mode, terminate and reset */
    typedef fmi2Status fmi2SetupExperimentTYPE       (fmi2Component c,
                                                      fmi2Boolean toleranceDefined,
                                                      fmi2Real tolerance,
                                                      fmi2Real startTime,
                                                      fmi2Boolean stopTimeDefined,
                                                      fmi2Real stopTime);
   typedef fmi2Status fmi2EnterInitializationModeTYPE(fmi2Component c);
   typedef fmi2Status fmi2ExitInitializationModeTYPE (fmi2Component c);
   typedef fmi2Status fmi2TerminateTYPE              (fmi2Component c);
   typedef fmi2Status fmi2ResetTYPE                  (fmi2Component c);

/* Getting and setting variable values */
   typedef fmi2Status fmi2GetRealTYPE   (fmi2Component c, const fmi2ValueReference vr[], size_t nvr, fmi2Real    value[]);
   typedef fmi2Status fmi2GetIntegerTYPE(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, fmi2Integer value[]);
   typedef fmi2Status fmi2GetBooleanTYPE(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, fmi2Boolean value[]);
   typedef fmi2Status fmi2GetStringTYPE (fmi2Component c, const fmi2ValueReference vr[], size_t nvr, fmi2String  value[]);

   typedef fmi2Status fmi2SetRealTYPE   (fmi2Component c, const fmi2ValueReference vr[], size_t nvr, const fmi2Real    value[]);
   typedef fmi2Status fmi2SetIntegerTYPE(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, const fmi2Integer value[]);
   typedef fmi2Status fmi2SetBooleanTYPE(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, const fmi2Boolean value[]);
   typedef fmi2Status fmi2SetStringTYPE (fmi2Component c, const fmi2ValueReference vr[], size_t nvr, const fmi2String  value[]);

/* Getting and setting the internal FMU state */
   typedef fmi2Status fmi2GetFMUstateTYPE           (fmi2Component c, fmi2FMUstate* FMUstate);
   typedef fmi2Status fmi2SetFMUstateTYPE           (fmi2Component c, fmi2FMUstate  FMUstate);
   typedef fmi2Status fmi2FreeFMUstateTYPE          (fmi2Component c, fmi2FMUstate* FMUstate);
   typedef fmi2Status fmi2SerializedFMUstateSizeTYPE(fmi2Component c, fmi2FMUstate  FMUstate, size_t* size);
   typedef fmi2Status fmi2SerializeFMUstateTYPE     (fmi2Component c, fmi2FMUstate  FMUstate, fmi2Byte[], size_t size);
   typedef fmi2Status fmi2DeSerializeFMUstateTYPE   (fmi2Component c, const fmi2Byte serializedState[], size_t size, fmi2FMUstate* FMUstate);

/* Getting partial derivatives */
    typedef fmi2Status fmi2GetDirectionalDerivativeTYPE(fmi2Component c,
                                                        const fmi2ValueReference vUnknown_ref[], size_t nUnknown,
                                                        const fmi2ValueReference vKnown_ref[],   size_t nKnown,
                                                        const fmi2Real dvKnown[],
                                                        fmi2Real dvUnknown[]);

/***************************************************
Types for Functions for FMI2 for Model Exchange
****************************************************/

/* Enter and exit the different modes */
   typedef fmi2Status fmi2EnterEventModeTYPE         (fmi2Component c);
   typedef fmi2Status fmi2NewDiscreteStatesTYPE      (fmi2Component c, fmi2EventInfo* fmi2eventInfo);
   typedef fmi2Status fmi2EnterContinuousTimeModeTYPE(fmi2Component c);
   typedef fmi2Status fmi2CompletedIntegratorStepTYPE(fmi2Component c,
                                                      fmi2Boolean   noSetFMUStatePriorToCurrentPoint,
                                                      fmi2Boolean*  enterEventMode,
                                                      fmi2Boolean*  terminateSimulation);

/* Providing independent variables and re-initialization of caching */
   typedef fmi2Status fmi2SetTimeTYPE            (fmi2Component c, fmi2Real time);
   typedef fmi2Status fmi2SetContinuousStatesTYPE(fmi2Component c, const fmi2Real x[], size_t nx);

/* Evaluation of the model equations */
   typedef fmi2Status fmi2GetDerivativesTYPE               (fmi2Component c, fmi2Real derivatives[],     size_t nx);
   typedef fmi2Status fmi2GetEventIndicatorsTYPE           (fmi2Component c, fmi2Real eventIndicators[], size_t ni);
   typedef fmi2Status fmi2GetContinuousStatesTYPE          (fmi2Component c, fmi2Real x[],               size_t nx);
   typedef fmi2Status fmi2GetNominalsOfContinuousStatesTYPE(fmi2Component c, fmi2Real x_nominal[],       size_t nx);


/***************************************************
Types for Functions for FMI2 for Co-Simulation
****************************************************/

/* Simulating the slave */
    typedef fmi2Status fmi2SetRealInputDerivativesTYPE (fmi2Component c,
                                                        const fmi2ValueReference vr[], size_t nvr,
                                                        const fmi2Integer order[],
                                                        const fmi2Real value[]);
    typedef fmi2Status fmi2GetRealOutputDerivativesTYPE(fmi2Component c,
                                                        const fmi2ValueReference vr[], size_t nvr,
                                                        const fmi2Integer order[],
                                                        fmi2Real value[]);
    typedef fmi2Status fmi2DoStepTYPE   (fmi2Component c,
                                         fmi2Real      currentCommunicationPoint,
                                         fmi2Real      communicationStepSize,
                                         fmi2Boolean   noSetFMUStatePriorToCurrentPoint);
   typedef fmi2Status fmi2CancelStepTYPE(fmi2Component c);

/* Inquire slave status */
   typedef fmi2Status fmi2GetStatusTYPE       (fmi2Component c, const fmi2StatusKind s, fmi2Status*  value);
   typedef fmi2Status fmi2GetRealStatusTYPE   (fmi2Component c, const fmi2StatusKind s, fmi2Real*    value);
   typedef fmi2Status fmi2GetIntegerStatusTYPE(fmi2Component c, const fmi2StatusKind s, fmi2Integer* value);
   typedef fmi2Status fmi2GetBooleanStatusTYPE(fmi2Component c, const fmi2StatusKind s, fmi2Boolean* value);
   typedef fmi2Status fmi2GetStringStatusTYPE (fmi2Component c, const fmi2StatusKind s, fmi2String*  value);


#ifdef __cplusplus
}  /* end of extern "C" { */
#endif

#endif /* fmi2FunctionTypes_h */
'''


###############################################################################
# fmi2TypesPlatform.h
###############################################################################
fmi2TypesPlatform_h = '''#ifndef fmi2TypesPlatform_h
#define fmi2TypesPlatform_h

/* Standard header file to define the argument types of the
   functions of the Functional Mock-up Interface 2.0.2
   This header file must be utilized both by the model and
   by the simulation engine.

   Revisions:
   - Sep. 29, 2019:  License changed to 2-clause BSD License (without extensions)
   - Apr.  9, 2014:  All prefixes "fmi" renamed to "fmi2" (decision from April 8)
   - Mar   31, 2014: New datatype fmiChar introduced.
   - Feb.  17, 2013: Changed fmiTypesPlatform from "standard32" to "default".
                     Removed fmiUndefinedValueReference since no longer needed
                     (because every state is defined in ScalarVariables).
   - March 20, 2012: Renamed from fmiPlatformTypes.h to fmiTypesPlatform.h
   - Nov.  14, 2011: Use the header file "fmiPlatformTypes.h" for FMI 2.0
                     both for "FMI for model exchange" and for "FMI for co-simulation"
                     New types "fmiComponentEnvironment", "fmiState", and "fmiByte".
                     The implementation of "fmiBoolean" is change from "char" to "int".
                     The #define "fmiPlatform" changed to "fmiTypesPlatform"
                     (in order that #define and function call are consistent)
   - Oct.   4, 2010: Renamed header file from "fmiModelTypes.h" to fmiPlatformTypes.h"
                     for the co-simulation interface
   - Jan.   4, 2010: Renamed meModelTypes_h to fmiModelTypes_h (by Mauss, QTronic)
   - Dec.  21, 2009: Changed "me" to "fmi" and "meModel" to "fmiComponent"
                     according to meeting on Dec. 18 (by Martin Otter, DLR)
   - Dec.   6, 2009: Added meUndefinedValueReference (by Martin Otter, DLR)
   - Sept.  9, 2009: Changes according to FMI-meeting on July 21:
                     Changed "version" to "platform", "standard" to "standard32",
                     Added a precise definition of "standard32" as comment
                     (by Martin Otter, DLR)
   - July  19, 2009: Added "me" as prefix to file names, added meTrue/meFalse,
                     and changed meValueReferenced from int to unsigned int
                     (by Martin Otter, DLR).
   - March  2, 2009: Moved enums and function pointer definitions to
                     ModelFunctions.h (by Martin Otter, DLR).
   - Dec.  3, 2008 : First version by Martin Otter (DLR) and
                     Hans Olsson (Dynasim).


   Copyright (C) 2008-2011 MODELISAR consortium,
                 2012-2020 Modelica Association Project "FMI"
                 All rights reserved.

   This file is licensed by the copyright holders under the 2-Clause BSD License
   (https://opensource.org/licenses/BSD-2-Clause):

   ----------------------------------------------------------------------------
   Redistribution and use in source and binary forms, with or without
   modification, are permitted provided that the following conditions are met:

   - Redistributions of source code must retain the above copyright notice,
     this list of conditions and the following disclaimer.

   - Redistributions in binary form must reproduce the above copyright notice,
     this list of conditions and the following disclaimer in the documentation
     and/or other materials provided with the distribution.

   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
   "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
   TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
   PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
   CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
   EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
   OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
   WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
   OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
   ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
   ----------------------------------------------------------------------------
*/

/* Platform (unique identification of this header file) */
#define fmi2TypesPlatform "default"

/* Type definitions of variables passed as arguments
   Version "default" means:

   fmi2Component           : an opaque object pointer
   fmi2ComponentEnvironment: an opaque object pointer
   fmi2FMUstate            : an opaque object pointer
   fmi2ValueReference      : handle to the value of a variable
   fmi2Real                : double precision floating-point data type
   fmi2Integer             : basic signed integer data type
   fmi2Boolean             : basic signed integer data type
   fmi2Char                : character data type
   fmi2String              : a pointer to a vector of fmi2Char characters
                             ('\0' terminated, UTF8 encoded)
   fmi2Byte                : smallest addressable unit of the machine, typically one byte.
*/
   typedef void*           fmi2Component;               /* Pointer to FMU instance       */
   typedef void*           fmi2ComponentEnvironment;    /* Pointer to FMU environment    */
   typedef void*           fmi2FMUstate;                /* Pointer to internal FMU state */
   typedef unsigned int    fmi2ValueReference;
   typedef double          fmi2Real   ;
   typedef int             fmi2Integer;
   typedef int             fmi2Boolean;
   typedef char            fmi2Char;
   typedef const fmi2Char* fmi2String;
   typedef char            fmi2Byte;

/* Values for fmi2Boolean  */
#define fmi2True  1
#define fmi2False 0


#endif /* fmi2TypesPlatform_h */
'''