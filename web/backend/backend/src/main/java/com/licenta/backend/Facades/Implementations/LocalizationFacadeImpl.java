package com.licenta.backend.Facades.Implementations;

import com.licenta.backend.Converter.LocalizationConverter;
import com.licenta.backend.Facades.LocalizationFacade;
import com.licenta.backend.Model.LocalizationRecord;
import com.licenta.backend.Service.LocalizationService;
import com.licenta.backend.dto.LocalizationDTO;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

@Component
@RequiredArgsConstructor
public class LocalizationFacadeImpl implements LocalizationFacade {
    private final LocalizationService localizationService;
    private final LocalizationConverter localizationConverter;
    private static final String QUERY_FOLDER="A:\\LICENTA\\Licenta\\processor\\dataset\\query";
    @Override
    public LocalizationDTO processAndSaveUpload(MultipartFile file, String uploaderId) throws IOException {
        File directory=new File(QUERY_FOLDER);
        if(!directory.exists()){
            directory.mkdirs();
        }
        Path filePath= Paths.get(QUERY_FOLDER,"query_test.png");
        Files.deleteIfExists(filePath);
        file.transferTo(filePath.toFile());
        LocalizationRecord record=localizationService.createAndSaveRecord(uploaderId);
        return localizationConverter.entityToDTO(record);
    }
}
