package dev.vanadium.speedtest;

import java.io.IOException;

public class Testing {

    static SpeedTestResult runTest() {
        ProcessDetails pd;
        try {
            pd = ProcessDetails.run("speedtest --secure --simple --no-pre-allocate");
        } catch (IOException | InterruptedException e) {
            throw new RuntimeException(e);
        }
        if (pd == null)
            return null;

        if (pd.getStatus() == ProcessStatus.EXEC_FAIL)
            return null;

        try {
            return Parser.parse(pd.getOutput());
        } catch (Exception e) {
            Log.log("Failed to parse speed test results: " + e.getMessage());
        }

        return null;
    }

    static SpeedTestResult runTestRetry(int times) {
        SpeedTestResult res = null;
        for (int i = 0; i < times; i ++) {
            res = runTest();
            if (res != null) {
                if (i > 0)
                    Log.log("Error resolved.");
                break;
            }
            else if (i + 1 < times) {
                Log.log("Speed test failed. Retrying (" + (i + 1) + "/" + times + ") ...");
            }
        }
        if (res == null)
            Log.log("Speed test still fails after " + times + " retries.");
        return res;
    }

}
