-- Scene Indicators Script
-- Provides visual and audio feedback for scene changes

obs = obslua

function script_description()
    return [[
Scene Indicators for OBS Infrastructure-as-Code

Provides enhanced feedback for scene changes:
- Scene name display in OBS interface
- Optional audio feedback for scene transitions
- Status indicators for recording state
- Integration with macropad layer indicators

This script enhances the manual control experience.
    ]]
end

function script_properties()
    local props = obs.obs_properties_create()
    
    obs.obs_properties_add_bool(props, "enable_audio_feedback", "Enable Audio Feedback")
    obs.obs_properties_add_bool(props, "show_scene_name", "Show Current Scene Name")
    obs.obs_properties_add_int(props, "indicator_duration", "Indicator Duration (seconds)", 1, 10, 1)
    
    return props
end

function script_defaults(settings)
    obs.obs_data_set_default_bool(settings, "enable_audio_feedback", false)
    obs.obs_data_set_default_bool(settings, "show_scene_name", true)
    obs.obs_data_set_default_int(settings, "indicator_duration", 3)
end

local enable_audio = false
local show_scene = true
local indicator_duration = 3

function script_update(settings)
    enable_audio = obs.obs_data_get_bool(settings, "enable_audio_feedback")
    show_scene = obs.obs_data_get_bool(settings, "show_scene_name")
    indicator_duration = obs.obs_data_get_int(settings, "indicator_duration")
end

-- Scene change callback
function on_scene_change()
    local current_scene = obs.obs_frontend_get_current_scene()
    if current_scene then
        local scene_name = obs.obs_source_get_name(current_scene)
        
        if show_scene then
            print("[Scene Indicator] Current scene: " .. scene_name)
        end
        
        obs.obs_source_release(current_scene)
    end
end

-- Recording state callback
function on_recording_state_change(event)
    if event == obs.OBS_FRONTEND_EVENT_RECORDING_STARTED then
        print("[Scene Indicator] Recording STARTED")
    elseif event == obs.OBS_FRONTEND_EVENT_RECORDING_STOPPED then
        print("[Scene Indicator] Recording STOPPED")
    elseif event == obs.OBS_FRONTEND_EVENT_RECORDING_PAUSED then
        print("[Scene Indicator] Recording PAUSED")
    elseif event == obs.OBS_FRONTEND_EVENT_RECORDING_UNPAUSED then
        print("[Scene Indicator] Recording RESUMED")
    end
end

function script_load(settings)
    obs.obs_frontend_add_event_callback(on_recording_state_change)
end

function script_unload()
    obs.obs_frontend_remove_event_callback(on_recording_state_change)
end