package com.licenta.backend.Service;

import com.licenta.backend.Model.LocalizationRecord;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;

public interface LocalizationService {
    LocalizationRecord createAndSaveRecord(String uploaderId);
    void updateStatus(Long recordId, String newStatus);
}
