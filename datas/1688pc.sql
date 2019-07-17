/*
 Navicat MySQL Data Transfer

 Source Server         : 树莓派数据库
 Source Server Type    : MySQL
 Source Server Version : 100138
 Source Host           : 192.168.0.220:3306
 Source Schema         : 1688

 Target Server Type    : MySQL
 Target Server Version : 100138
 File Encoding         : 65001

 Date: 15/07/2019 16:44:44
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for 1688pc
-- ----------------------------
DROP TABLE IF EXISTS `1688pc`;
CREATE TABLE `1688pc`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '商品标题',
  `weight` int(3) NULL DEFAULT NULL COMMENT '选择权重',
  `image_url` varchar(90) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '商品图片链接',
  `ads_url` varchar(800) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '原商品链接',
  `url` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '解析地址',
  `supplier` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '供应商名称',
  `is_niu` tinyint(1) NULL DEFAULT NULL COMMENT '是否为实力商家',
  `years` int(3) NULL DEFAULT NULL COMMENT '成立年限',
  `amount_30` decimal(10, 2) NULL DEFAULT NULL COMMENT '30天内成交额',
  `rebuy` decimal(5, 4) NULL DEFAULT NULL COMMENT '回头率',
  `model` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '经营模式',
  `price1` decimal(10, 2) NULL DEFAULT NULL COMMENT '价格1',
  `condition1` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '采购量1',
  `price2` decimal(10, 2) NULL DEFAULT NULL COMMENT '价格2',
  `condition2` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '采购量2',
  `price3` decimal(10, 2) NULL DEFAULT NULL COMMENT '价格3',
  `condition3` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '采购量3',
  `desc` decimal(5, 4) NULL DEFAULT NULL COMMENT '货描',
  `response` decimal(5, 4) NULL DEFAULT NULL COMMENT '响应',
  `delivery` decimal(5, 4) NULL DEFAULT NULL COMMENT '发货',
  `crawel_date` date NULL DEFAULT NULL COMMENT '入库日期',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Compact;

SET FOREIGN_KEY_CHECKS = 1;
