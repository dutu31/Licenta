package com.licenta.backend.Service.Implementations;

import com.licenta.backend.Service.FileStorageService;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.UUID;
@Service
public class FileStorageServiceImpl implements FileStorageService {
    private final String UploadDir="A:\\LICENTA\\videos";

    @Override
    public String saveVideoFile(MultipartFile file) throws IOException {
        File directory=new File(UploadDir);
        if(!directory.exists()){
            directory.mkdirs();
        }
        String originalFilename=file.getOriginalFilename();
        String uniqueFilename= UUID.randomUUID().toString()+"."+originalFilename;
        Path filePath = Paths.get(UploadDir,uniqueFilename);
        Files.write(filePath,file.getBytes());
        return filePath.toString();
    }
}
