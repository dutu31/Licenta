package com.licenta.backend.Service;

import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;


public interface FileStorageService {
    String saveVideoFile(MultipartFile file) throws IOException;

}
