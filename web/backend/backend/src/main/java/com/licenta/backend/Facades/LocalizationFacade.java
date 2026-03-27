package com.licenta.backend.Facades;

import com.licenta.backend.dto.LocalizationDTO;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;

public interface LocalizationFacade {
    public LocalizationDTO processAndSaveUpload(MultipartFile file, String uploaderId) throws IOException;
}
