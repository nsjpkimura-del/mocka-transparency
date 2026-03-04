# MoCKA Transparency

MoCKA Transparency is the public verification and audit layer of the MoCKA Ecosystem.

It exposes cryptographic proofs, timestamp anchors, and integrity logs in a form that external observers can independently verify.

This repository does not execute or govern.
It proves.

## Architecture Overview

Transparency connects deterministic artifacts from MoCKA and canonical traces from Knowledge Gate to external verifiers.

![MoCKA Architecture Overview](docs/architecture/mocka_architecture_overview.png)

## Security Model

Threat assumptions:

- Undetected artifact tampering
- Loss of public verifiability
- Timestamp forgery
- Observer asymmetry (internal vs external knowledge gap)

Controls:

- Hash publication (SHA-256 integrity anchors)
- RFC3161 timestamp anchoring (where applicable)
- Signed verification packs
- Independent reproducibility of verification scripts

Transparency assumes that trust must be earned through verifiability.

## Repository Responsibility

This repository focuses on:

- Publishing integrity hashes
- Timestamp references
- Public verification scripts
- Audit-ready export artifacts

It is optimized for external inspection.

## Relationship to Ecosystem

- MoCKA: produces deterministic artifacts
- Knowledge Gate: preserves canonical traces
- Civilization: defines governance rules
- External Brain: may consume public proofs

---

# MoCKA Transparency（日本語）

MoCKA Transparency は、MoCKA エコシステムの公開検証層です。

暗号学的証明、タイムスタンプ固定、完全性ログを外部監査者が独立検証できる形で公開します。

本リポジトリは実行もしません。
統治もしません。
証明します。

## Architecture Overview（全体図）

Transparency は、MoCKA の決定成果物と Knowledge Gate の正本痕跡を外部検証者へ接続します。

![MoCKA Architecture Overview](docs/architecture/mocka_architecture_overview.png)

## Security Model（脅威と対策）

想定脅威：

- 成果物改ざんの未検知
- 公開検証性の喪失
- タイムスタンプ偽造
- 内外の情報非対称性

対策：

- SHA-256 完全性ハッシュ公開
- RFC3161 タイムスタンプ固定（適用可能な場合）
- 署名付き検証パック
- 独立再現可能な検証スクリプト

Transparency は信頼を前提にしません。
検証を前提にします。

## 本リポジトリの責務

- 完全性ハッシュの公開
- タイムスタンプ参照の提示
- 公開検証スクリプトの提供
- 監査対応エクスポートの維持

外部検査に最適化されています。

## エコシステム関係

- MoCKA：決定成果物生成
- Knowledge Gate：正本保存
- Civilization：統治定義
- External Brain：公開証明の利用
