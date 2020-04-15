# MigrateToAndroidX

用于帮助迁移到AndroidX。

## 前言
通过Android Studio提供的Migrate to AndroidX功能并不能很好地处理所有文件，所以才有了此脚本。原理：通过Android官方网站提供的类映射关系，扫描工程中所有文件进行替换。

## 使用

在gradle.properties文件中添加以下属性：
```
android.useAndroidX=true //表示启用androidx
android.enableJetifier=true //会对依赖库进行迁移

```
还可以添加`android.jetifier.blacklist=xxx.jar`来跳过某些不兼容且确定不需要转换的lib

对工程进行Sync确保依赖库已经改为androidx。
拷贝文件到项目父路径，会扫描.py同级目录下的所有子目录，

```
实际的目录:
root
-migrate.py
-androidx-class-mapping.csv
-项目
 |-app
 |-build.gradle
 |-其他文件
```



打开终端在工程根目录执行以下命令：

```

python migrate.py
```

获取最新的映射文件 https://developer.android.com/jetpack/androidx/migrate/class-mappings

## 不支持

- 不支持依赖替换
- 不支持多行导包替换  

fork from:github.com:yuweiguocn/MigrateToAndroidX