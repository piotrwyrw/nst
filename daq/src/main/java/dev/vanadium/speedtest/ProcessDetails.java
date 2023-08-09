package dev.vanadium.speedtest;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

public class ProcessDetails {

    private ProcessStatus status;
    private int exitValue;
    private String output;

    public ProcessDetails(ProcessStatus status, int exitValue, String output) {
        this.status = status;
        this.exitValue = exitValue;
        this.output = output;
    }

    public static ProcessDetails run(String cmd) throws IOException, InterruptedException {
        cmd = cmd.trim();
        Process proc = null;
        try {
            proc = new ProcessBuilder((cmd).split("\\s+")).start();
        } catch (IOException e) {
            Log.log("Failed to run process: " + e.getClass().getSimpleName());
            return null;
        }
        InputStream rslt = proc.getInputStream();
        BufferedReader reader = new BufferedReader(new InputStreamReader(rslt));
        StringBuilder builder = new StringBuilder();
        String tmp;
        Log.log("Running process '" + cmd +  "' ...");
        int termVal = proc.waitFor();
        while ((tmp = reader.readLine()) != null)
            builder.append(tmp).append('\n');

        String s = builder.toString();

        return new ProcessDetails((termVal == 0) ? ProcessStatus.OK : ProcessStatus.EXEC_FAIL, termVal, s);
    }

    public ProcessStatus getStatus() {
        return status;
    }

    public int getExitValue() {
        return exitValue;
    }

    public String getOutput() {
        return output;
    }
}
