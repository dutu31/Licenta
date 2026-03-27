package com.licenta.backend.Service.Implementations;

import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;

@Service
public class SfmService {
    private final String workspacePath="A:\\LICENTA\\Licenta\\processor";
    private final String pythonExe="A:\\LICENTA\\Licenta\\processor\\venv\\Scripts\\python.exe";
    public boolean executePythonScript(String scriptName){
        try {
            ProcessBuilder pb=new ProcessBuilder(pythonExe,scriptName);
            pb.directory(new File(workspacePath));
            pb.redirectErrorStream(true);
            Process process= pb.start();
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println("[PYTHON] " + line);
            }
            int exitCode= process.waitFor();
            System.out.println("PYTHON script finished with code: " + exitCode);
            return exitCode == 0;
        } catch (Exception e) {
            System.out.println("[ERROR] " + e.getMessage());
            e.printStackTrace();
            return false;
        }

    }

}
