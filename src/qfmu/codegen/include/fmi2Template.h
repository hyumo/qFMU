/* ---------------------------------------------------------------------------*
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