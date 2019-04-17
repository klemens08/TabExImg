import os
import shutil


class FileHelper:

    @staticmethod
    def getRelativeDirPath(absolute_file_path, base_path):
        # get relative directory path e.g. /eu-01
        dir_path = os.path.dirname(absolute_file_path)
        rel_dir = os.path.relpath(dir_path, base_path)
        return rel_dir

    @staticmethod
    def createSubdirectoriesIfNecessary(base_dir, rel_dir):
        directory = os.path.join(base_dir, rel_dir)
        # create subdirectories if not exist for preprocessed and original images
        if not os.path.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def moveInputFiles(source_folder_path, destination_folder_path, image_path, rel_dir):
        absolute_destination_path = os.path.join(destination_folder_path, image_path)
        absolute_source_folder_path = os.path.join(source_folder_path, rel_dir, image_path)
        FileHelper.createSubdirectoriesIfNecessary(destination_folder_path, rel_dir)
        # move file from input to processed image directory
        os.rename(absolute_source_folder_path, absolute_destination_path)

        input_dir = os.path.join(source_folder_path, rel_dir)
        if not os.listdir(input_dir):
            os.rmdir(input_dir)

    @staticmethod
    def moveFiles(source_folder, destination_folder):
        files = os.listdir(source_folder)
        for file in files:
            shutil.move(os.path.join(source_folder, file), destination_folder)

    @staticmethod
    def getAllFilesInFolder(folder):
        files = os.listdir(folder)
        return files

    @staticmethod
    def getFilesRecursive(root):
        file_set = set()
        for dir_, _, files in os.walk(root):
            for file_name in files:
                file = os.path.join(root, dir_, file_name)
                file_set.add(file)
        return file_set

    @staticmethod
    def deleteAllFilesInFolder(folder):
        files = FileHelper.getFilesRecursive(folder)
        for file in files:
            os.remove(file)

        filelist = [f for f in os.listdir(folder)]
        for f in filelist:
            os.rmdir(os.path.join(folder, f))

    @staticmethod
    def createPathIfNotExisting(path):
        if not os.path.exists(path):
            os.makedirs(path)


