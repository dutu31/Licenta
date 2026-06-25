package com.licenta.backend.Controller;

import com.licenta.backend.Facades.LocalizationFacade;
import com.licenta.backend.Service.Implementations.SfmService;
import com.licenta.backend.dto.LocalizationDTO;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api/localization")
@RequiredArgsConstructor
@CrossOrigin(origins="http://localhost:3000")
public class LocalizationController {
    private final SfmService sfmService;
    private final LocalizationFacade localizationFacade;
    private static final String QUERY_FOLDER="A:\\LICENTA\\Licenta\\processor\\dataset\\query";

    @PostMapping("/upload")
    public ResponseEntity<?> uploadQueryImage(
            @RequestParam("file") MultipartFile file,
            @RequestParam("uploaderId") String uploaderId) {
        try {
            LocalizationDTO response = localizationFacade.processAndSaveUpload(file, uploaderId);
            return ResponseEntity.ok(response);

        } catch(Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body("Error at saving image! " + e.getMessage());
        }
    }

    @PostMapping("/run-localize")
    public ResponseEntity<String> runLocalize(){
        System.out.println("Running localize script...");
        boolean isSuccess= sfmService.executePythonScript("localize.py");
        if(isSuccess){
            return ResponseEntity.status(HttpStatus.OK).body("Localize script executed successfully!");
        } else {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("COLMAP couldn't localize the image!");
        }
    }

    @PostMapping("/view")
    public ResponseEntity<String> viewLocation(){
        System.out.println("Running view script...");
        boolean isSuccess= sfmService.executePythonScript("viewer.py");
        if(isSuccess){
            return ResponseEntity.ok("Viewer script executed successfully!");
        } else {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error at viewing image!");
        }
    }
}
