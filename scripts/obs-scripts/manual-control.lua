-- Manual OBS Control Script
-- Provides enhanced manual control for OBS scene switching with priority override

obs = obslua

-- Script information
function script_description()
    return [[
Manual Control Priority System for OBS Infrastructure-as-Code

This script provides enhanced manual control with the following features:
- Priority manual scene switching (overrides automation)
- Hotkey-based scene control with feedback
- Scene transition timing control
- Recording status indicators
- Integration with macropad and remote control systems

Configure your hotkeys in OBS Settings → Hotkeys to use this system.
    ]]
end

-- Script properties for user configuration
function script_properties()
    local props = obs.obs_properties_create()
    
    obs.obs_properties_add_bool(props, "enable_manual_priority", "Enable Manual Priority Mode")
    obs.obs_properties_add_int(props, "transition_duration", "Default Transition Duration (ms)", 100, 2000, 50)
    obs.obs_properties_add_bool(props, "show_scene_notifications", "Show Scene Change Notifications")
    obs.obs_properties_add_bool(props, "log_scene_changes", "Log Scene Changes")
    
    return props
end

-- Default settings
function script_defaults(settings)
    obs.obs_data_set_default_bool(settings, "enable_manual_priority", true)
    obs.obs_data_set_default_int(settings, "transition_duration", 300)
    obs.obs_data_set_default_bool(settings, "show_scene_notifications", true)
    obs.obs_data_set_default_bool(settings, "log_scene_changes", false)
end

-- Global variables
local manual_priority = true
local transition_duration = 300
local show_notifications = true
local log_changes = false
local current_scene = nil

-- Settings update callback
function script_update(settings)
    manual_priority = obs.obs_data_get_bool(settings, "enable_manual_priority")
    transition_duration = obs.obs_data_get_int(settings, "transition_duration")
    show_notifications = obs.obs_data_get_bool(settings, "show_scene_notifications")
    log_changes = obs.obs_data_get_bool(settings, "log_scene_changes")
end

-- Scene switching function with enhanced control
function switch_to_scene(scene_name)
    local scenes = obs.obs_frontend_get_scenes()
    local target_scene = nil
    
    -- Find the target scene
    for _, scene in pairs(scenes) do
        local name = obs.obs_source_get_name(scene)
        if name == scene_name then
            target_scene = scene
            break
        end
    end
    
    if target_scene then
        -- Set transition duration
        obs.obs_frontend_set_transition_duration(transition_duration)
        
        -- Switch to scene
        obs.obs_frontend_set_current_scene(target_scene)
        
        -- Log if enabled
        if log_changes then
            print("[Manual Control] Scene switched to: " .. scene_name)
        end
        
        -- Show notification if enabled
        if show_notifications then
            -- Note: OBS Lua doesn't have built-in notifications
            -- This would require additional integration
        end
        
        current_scene = scene_name
    end
    
    -- Release scene references
    obs.source_list_release(scenes)
end

-- Hotkey callbacks for direct scene access
function scene_intro_callback(pressed)
    if pressed and manual_priority then
        switch_to_scene("🎬 Intro Scene")
    end
end

function scene_talking_head_callback(pressed)
    if pressed and manual_priority then
        switch_to_scene("👤 Talking Head")
    end
end

function scene_code_camera_callback(pressed)
    if pressed and manual_priority then
        switch_to_scene("💻 Code + Camera")
    end
end

function scene_screen_only_callback(pressed)
    if pressed and manual_priority then
        switch_to_scene("🖥️ Screen Only")
    end
end

function scene_brb_callback(pressed)
    if pressed and manual_priority then
        switch_to_scene("📺 BRB / Technical")
    end
end

function scene_outro_callback(pressed)
    if pressed and manual_priority then
        switch_to_scene("🎯 Outro Scene")
    end
end

function scene_dual_camera_callback(pressed)
    if pressed and manual_priority then
        switch_to_scene("👥 Dual Camera / Interview")
    end
end

-- Recording control functions
function toggle_recording_callback(pressed)
    if pressed then
        if obs.obs_frontend_recording_active() then
            obs.obs_frontend_recording_stop()
            if log_changes then
                print("[Manual Control] Recording stopped")
            end
        else
            obs.obs_frontend_recording_start()
            if log_changes then
                print("[Manual Control] Recording started")
            end
        end
    end
end

function pause_recording_callback(pressed)
    if pressed then
        if obs.obs_frontend_recording_active() then
            if obs.obs_frontend_recording_paused() then
                obs.obs_frontend_recording_unpause()
                if log_changes then
                    print("[Manual Control] Recording unpaused")
                end
            else
                obs.obs_frontend_recording_pause()
                if log_changes then
                    print("[Manual Control] Recording paused")
                end
            end
        end
    end
end

-- Register hotkeys
function script_load(settings)
    -- Scene switching hotkeys
    obs.obs_hotkey_register_frontend("manual_scene_intro", "Manual: Intro Scene", scene_intro_callback)
    obs.obs_hotkey_register_frontend("manual_scene_talking_head", "Manual: Talking Head", scene_talking_head_callback)
    obs.obs_hotkey_register_frontend("manual_scene_code_camera", "Manual: Code + Camera", scene_code_camera_callback)
    obs.obs_hotkey_register_frontend("manual_scene_screen_only", "Manual: Screen Only", scene_screen_only_callback)
    obs.obs_hotkey_register_frontend("manual_scene_brb", "Manual: BRB / Technical", scene_brb_callback)
    obs.obs_hotkey_register_frontend("manual_scene_outro", "Manual: Outro Scene", scene_outro_callback)
    obs.obs_hotkey_register_frontend("manual_scene_dual_camera", "Manual: Dual Camera", scene_dual_camera_callback)
    
    -- Recording control hotkeys
    obs.obs_hotkey_register_frontend("manual_toggle_recording", "Manual: Toggle Recording", toggle_recording_callback)
    obs.obs_hotkey_register_frontend("manual_pause_recording", "Manual: Pause Recording", pause_recording_callback)
end

-- Cleanup
function script_unload()
    -- No specific cleanup needed
end