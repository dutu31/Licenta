package com.licenta.backend.Repository;

import com.licenta.backend.Model.LocalizationRecord;
import org.springframework.data.jpa.repository.JpaRepository;

public interface LocalizationRecordRepository extends JpaRepository<LocalizationRecord, Long> {
}
