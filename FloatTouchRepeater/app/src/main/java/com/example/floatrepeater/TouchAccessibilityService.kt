package com.example.floatrepeater

import android.accessibilityservice.AccessibilityService
import android.accessibilityservice.GestureDescription
import android.graphics.Path
import android.view.accessibility.AccessibilityEvent

class TouchAccessibilityService : AccessibilityService() {

    private var lastX: Float = 0f
    private var lastY: Float = 0f

    override fun onAccessibilityEvent(event: AccessibilityEvent?) {
        // Placeholder: capture coordinates of recent touch events
        // Actual implementation may require more complex gesture detection
    }

    override fun onInterrupt() {}

    fun performLastGesture() {
        val path = Path().apply {
            moveTo(lastX, lastY)
            lineTo(lastX, lastY)
        }
        val gesture = GestureDescription.Builder()
            .addStroke(GestureDescription.StrokeDescription(path, 0, 1))
            .build()
        dispatchGesture(gesture, null, null)
    }

    override fun onServiceConnected() {
        instance = this
    }

    override fun onDestroy() {
        super.onDestroy()
        if (instance == this) instance = null
    }

    companion object {
        var instance: TouchAccessibilityService? = null
            private set
    }
}
