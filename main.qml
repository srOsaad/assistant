import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: showWind
    height: 600
    width: height
    color: "transparent"
    title: "Ai assistant"
    flags: Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
    property bool turnedOn: false
    property bool showWind: true
    property bool showLog: false

    Rectangle {
        anchors.centerIn: parent
        color: "black"
        rotation: 45
        width: Math.sqrt(Math.pow(parent.height, 2) * 0.5)
        height: width

        Rectangle {
            z: 4
            width: 150
            height: 150
            anchors.bottom: parent.bottom
            anchors.right: parent.right
            color: "transparent"

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    showLog = !showLog
                }
            }
        }

        Rectangle {
            color: "blue"
            anchors.centerIn: parent
            width: Math.sqrt(Math.pow(parent.height, 2) * 0.5)
            height: width
            rotation: -45
            visible: showLog
            z: 2

            Flickable {
                anchors.fill: parent
                contentHeight: log.height
                clip: true

                Text {
                    id: log
                    width: parent.width
                    color: "white"
                    text: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. " +
                          "Sed cursus ante dapibus diam. Sed nisi. Nulla quis sem at nibh elementum imperdiet. Duis sagittis ipsum."
                    wrapMode: Text.WordWrap
                    font.pixelSize: 15
                }
            }
        }

        Image {
            id: micIcon
            height: 80
            rotation: -45
            fillMode: Image.PreserveAspectFit
            source: turnedOn ? "components/on.png" : "components/off.png"
            anchors.centerIn: parent
            z: 1

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    turnedOn = !turnedOn;
                    waveEffect.visible = turnedOn;
                    if (turnedOn) bridge.on()
                    else bridge.off()
                }
                onPressAndHold: {
                    if (!turnedOn) Qt.quit()
                }
            }
        }

        AnimatedImage {
            id: waveEffect
            source: "components/listening.gif"
            rotation: 90
            width: parent.width
            height: parent.height
            anchors.centerIn: micIcon
            playing: turnedOn
            visible: false
            smooth: true
            fillMode: Image.PreserveAspectFit
            cache: true
        }
    }

    Connections {
        target: bridge
        function onShowApp(a) {
            showWind = a
        }
    }
}
