package dev.vanadium.speedtest;

import java.time.Instant;

public class SpeedTestResult {

    private double up;
    private double down;
    private double ping;
    private String actualTime;
    private long unix;

    public SpeedTestResult(double up, double down, double ping, String actualTime) {
        this.up = up;
        this.down = down;
        this.ping = ping;
        this.unix = Instant.now().getEpochSecond();
        this.actualTime = actualTime;
    }

    public double getUp() {
        return up;
    }

    public double getDown() {
        return down;
    }

    public double getPing() {
        return ping;
    }

    public String getActualTime() {
        return actualTime;
    }

    public long getUnix() {
        return unix;
    }
}
