package dev.vanadium.speedtest;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Files;
import java.util.ArrayList;

public class ResultsFile {

    private ArrayList<SpeedTestResult> results;

    public ResultsFile() {
        this.results = new ArrayList<>();
    }

    public void add(SpeedTestResult rslt) {
        results.add(rslt);
    }

    public void read(File file) {
        try {
            Gson gson = new Gson();
            ResultsFile res = gson.fromJson(new FileReader(file), getClass());
            this.results = res.results;
        } catch (FileNotFoundException e) {
            throw new RuntimeException(e);
        }
    }

    public void write(File file) {
        Gson gson = new GsonBuilder().setPrettyPrinting().create();
        try {
            Files.write(file.toPath(), gson.toJson(this).getBytes());
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public ArrayList<SpeedTestResult> getResults() {
        return results;
    }
}
