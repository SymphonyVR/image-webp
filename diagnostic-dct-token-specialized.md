# Specialized VP8 DCT verification diagnostic

```text
test=0
clippy=0
msrv=0
```

## Test tail
```text
[1m[92m   Compiling[0m quick-error v2.0.1
[1m[92m     Running[0m `/home/runner/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/bin/rustc --crate-name quick_error --edition=2018 /home/runner/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/quick-error-2.0.1/src/lib.rs --error-format=json --json=diagnostic-rendered-ansi,artifacts,future-incompat --crate-type lib --emit=dep-info,metadata,link -C embed-bitcode=no -C debuginfo=2 --check-cfg 'cfg(docsrs,test)' --check-cfg 'cfg(feature, values())' -C metadata=1a8dfa4e955b9d35 -C extra-filename=-d88c5aeea3a3d7d1 --out-dir /home/runner/work/image-webp/image-webp/target/debug/deps -L dependency=/home/runner/work/image-webp/image-webp/target/debug/deps --cap-lints allow`
[1m[92m   Compiling[0m png v0.17.16
[1m[92m     Running[0m `/home/runner/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/bin/rustc --crate-name png --edition=2018 /home/runner/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/png-0.17.16/src/lib.rs --error-format=json --json=diagnostic-rendered-ansi,artifacts,future-incompat --crate-type lib --emit=dep-info,metadata,link -C embed-bitcode=no -C debuginfo=2 --warn=unexpected_cfgs --check-cfg 'cfg(fuzzing)' --check-cfg 'cfg(docsrs,test)' --check-cfg 'cfg(feature, values("benchmarks", "unstable"))' -C metadata=f3d8e14db2441500 -C extra-filename=-e598a91edf8375c4 --out-dir /home/runner/work/image-webp/image-webp/target/debug/deps -L dependency=/home/runner/work/image-webp/image-webp/target/debug/deps --extern bitflags=/home/runner/work/image-webp/image-webp/target/debug/deps/libbitflags-cee6402aec96904c.rmeta --extern crc32fast=/home/runner/work/image-webp/image-webp/target/debug/deps/libcrc32fast-058d794bc137cb1e.rmeta --extern fdeflate=/home/runner/work/image-webp/image-webp/target/debug/deps/libfdeflate-00519c57695e7721.rmeta --extern flate2=/home/runner/work/image-webp/image-webp/target/debug/deps/libflate2-f83a9c677c4d9daa.rmeta --extern miniz_oxide=/home/runner/work/image-webp/image-webp/target/debug/deps/libminiz_oxide-f128a351df8360b7.rmeta --cap-lints allow`
[1m[92m   Compiling[0m rand v0.8.7
[1m[92m     Running[0m `/home/runner/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/bin/rustc --crate-name rand --edition=2018 /home/runner/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/rand-0.8.7/src/lib.rs --error-format=json --json=diagnostic-rendered-ansi,artifacts,future-incompat --crate-type lib --emit=dep-info,metadata,link -C embed-bitcode=no -C debuginfo=2 --cfg 'feature="alloc"' --cfg 'feature="default"' --cfg 'feature="getrandom"' --cfg 'feature="libc"' --cfg 'feature="rand_chacha"' --cfg 'feature="std"' --cfg 'feature="std_rng"' --check-cfg 'cfg(docsrs,test)' --check-cfg 'cfg(feature, values("alloc", "default", "getrandom", "libc", "log", "min_const_gen", "nightly", "rand_chacha", "serde", "serde1", "small_rng", "std", "std_rng"))' -C metadata=fbc79113d10e7bf7 -C extra-filename=-afaa0a85c24cc4e5 --out-dir /home/runner/work/image-webp/image-webp/target/debug/deps -L dependency=/home/runner/work/image-webp/image-webp/target/debug/deps --extern libc=/home/runner/work/image-webp/image-webp/target/debug/deps/liblibc-09aab59f5cb60a9d.rmeta --extern rand_chacha=/home/runner/work/image-webp/image-webp/target/debug/deps/librand_chacha-37203876d110984e.rmeta --extern rand_core=/home/runner/work/image-webp/image-webp/target/debug/deps/librand_core-2bf8e050a7796661.rmeta --cap-lints allow`
[1m[92m     Running[0m `/home/runner/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/bin/rustc --crate-name paste --edition=2018 /home/runner/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/paste-1.0.15/src/lib.rs --error-format=json --json=diagnostic-rendered-ansi,artifacts,future-incompat --crate-type proc-macro --emit=dep-info,link -C prefer-dynamic -C embed-bitcode=no --check-cfg 'cfg(docsrs,test)' --check-cfg 'cfg(feature, values())' -C metadata=75366573d83569d1 -C extra-filename=-594f55fe5cfdc9fd --out-dir /home/runner/work/image-webp/image-webp/target/debug/deps -L dependency=/home/runner/work/image-webp/image-webp/target/debug/deps --extern proc_macro --cap-lints allow --check-cfg 'cfg(no_literal_fromstr)' --check-cfg 'cfg(feature, values("protocol_feature_paste"))'`
[1m[92m   Compiling[0m image-webp v0.2.4 (/home/runner/work/image-webp/image-webp)
[1m[92m     Running[0m `/home/runner/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/bin/rustc --crate-name image_webp --edition=2021 src/lib.rs --error-format=json --json=diagnostic-rendered-ansi,artifacts,future-incompat --crate-type lib --emit=dep-info,metadata,link -C embed-bitcode=no -C debuginfo=2 --check-cfg 'cfg(docsrs,test)' --check-cfg 'cfg(feature, values("_benchmarks"))' -C metadata=d9ac2fe506a8ab32 -C extra-filename=-c2294830a6b5f4a4 --out-dir /home/runner/work/image-webp/image-webp/target/debug/deps -L dependency=/home/runner/work/image-webp/image-webp/target/debug/deps --extern byteorder_lite=/home/runner/work/image-webp/image-webp/target/debug/deps/libbyteorder_lite-a278a9f14042f35b.rmeta --extern quick_error=/home/runner/work/image-webp/image-webp/target/debug/deps/libquick_error-d88c5aeea3a3d7d1.rmeta`
[1m[92m   Compiling[0m image v0.25.10
[1m[92m     Running[0m `/home/runner/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/bin/rustc --crate-name image --edition=2021 /home/runner/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/image-0.25.10/src/lib.rs --error-format=json --json=diagnostic-rendered-ansi,artifacts,future-incompat --crate-type lib --emit=dep-info,metadata,link -C embed-bitcode=no -C debuginfo=2 --check-cfg 'cfg(docsrs,test)' --check-cfg 'cfg(feature, values("avif", "avif-native", "benchmarks", "bmp", "color_quant", "dds", "default", "default-formats", "exr", "ff", "gif", "hdr", "ico", "jpeg", "nasm", "png", "pnm", "qoi", "rayon", "serde", "tga", "tiff", "webp"))' -C metadata=f964da3de205906e -C extra-filename=-123946dce3f31416 --out-dir /home/runner/work/image-webp/image-webp/target/debug/deps -L dependency=/home/runner/work/image-webp/image-webp/target/debug/deps --extern bytemuck=/home/runner/work/image-webp/image-webp/target/debug/deps/libbytemuck-fea6388064e94308.rmeta --extern byteorder_lite=/home/runner/work/image-webp/image-webp/target/debug/deps/libbyteorder_lite-a278a9f14042f35b.rmeta --extern moxcms=/home/runner/work/image-webp/image-webp/target/debug/deps/libmoxcms-c15add4416a7deff.rmeta --extern num_traits=/home/runner/work/image-webp/image-webp/target/debug/deps/libnum_traits-576bc1e0d1c4ed8a.rmeta --cap-lints allow`
[1m[92m     Running[0m `/home/runner/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/bin/rustc --crate-name libwebp_sys --edition=2021 /home/runner/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/libwebp-sys-0.9.6/src/lib.rs --error-format=json --json=diagnostic-rendered-ansi,artifacts,future-incompat --crate-type lib --emit=dep-info,metadata,link -C embed-bitcode=no -C debuginfo=2 --cfg 'feature="default"' --cfg 'feature="neon"' --cfg 'feature="parallel"' --cfg 'feature="std"' --check-cfg 'cfg(docsrs,test)' --check-cfg 'cfg(feature, values("avx2", "default", "neon", "parallel", "sse41", "std"))' -C metadata=061c66db02839346 -C extra-filename=-ae911b6057dd70a0 --out-dir /home/runner/work/image-webp/image-webp/target/debug/deps -L dependency=/home/runner/work/image-webp/image-webp/target/debug/deps --cap-lints allow -L native=/home/runner/work/image-webp/image-webp/target/debug/build/libwebp-sys-7669b733598afc52/out -L native=/home/runner/work/image-webp/image-webp/target/debug/build/libwebp-sys-7669b733598afc52/out -l static=sharpyuv -l static=webpsys`
[1m[92m   Compiling[0m webp v0.3.1
[1m[92m     Running[0m `/home/runner/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/bin/rustc --crate-name webp --edition=2021 /home/runner/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/webp-0.3.1/src/lib.rs --error-format=json --json=diagnostic-rendered-ansi,artifacts,future-incompat --crate-type lib --emit=dep-info,metadata,link -C embed-bitcode=no -C debuginfo=2 --cfg 'feature="default"' --cfg 'feature="image"' --cfg 'feature="img"' --check-cfg 'cfg(docsrs,test)' --check-cfg 'cfg(feature, values("default", "image", "img"))' -C metadata=d765b91cc98f93a4 -C extra-filename=-7648140fa8b53cb3 --out-dir /home/runner/work/image-webp/image-webp/target/debug/deps -L dependency=/home/runner/work/image-webp/image-webp/target/debug/deps --extern image=/home/runner/work/image-webp/image-webp/target/debug/deps/libimage-123946dce3f31416.rmeta --extern libwebp_sys=/home/runner/work/image-webp/image-webp/target/debug/deps/liblibwebp_sys-ae911b6057dd70a0.rmeta --cap-lints allow -L native=/home/runner/work/image-webp/image-webp/target/debug/build/libwebp-sys-7669b733598afc52/out -L native=/home/runner/work/image-webp/image-webp/target/debug/build/libwebp-sys-7669b733598afc52/out`
[1m[92m     Running[0m `/home/runner/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/bin/rustc --crate-name image_webp --edition=2021 src/lib.rs --error-format=json --json=diagnostic-rendered-ansi,artifacts,future-incompat --emit=dep-info,link -C embed-bitcode=no -C debuginfo=2 --test --check-cfg 'cfg(docsrs,test)' --check-cfg 'cfg(feature, values("_benchmarks"))' -C metadata=d5c42d9322f5cb2d -C extra-filename=-5a4d9592037bd063 --out-dir /home/runner/work/image-webp/image-webp/target/debug/deps -L dependency=/home/runner/work/image-webp/image-webp/target/debug/deps --extern byteorder_lite=/home/runner/work/image-webp/image-webp/target/debug/deps/libbyteorder_lite-a278a9f14042f35b.rlib --extern paste=/home/runner/work/image-webp/image-webp/target/debug/deps/libpaste-594f55fe5cfdc9fd.so --extern png=/home/runner/work/image-webp/image-webp/target/debug/deps/libpng-e598a91edf8375c4.rlib --extern quick_error=/home/runner/work/image-webp/image-webp/target/debug/deps/libquick_error-d88c5aeea3a3d7d1.rlib --extern rand=/home/runner/work/image-webp/image-webp/target/debug/deps/librand-afaa0a85c24cc4e5.rlib --extern webp=/home/runner/work/image-webp/image-webp/target/debug/deps/libwebp-7648140fa8b53cb3.rlib -L native=/home/runner/work/image-webp/image-webp/target/debug/build/libwebp-sys-7669b733598afc52/out -L native=/home/runner/work/image-webp/image-webp/target/debug/build/libwebp-sys-7669b733598afc52/out`
[1m[92m     Running[0m `/home/runner/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/bin/rustc --crate-name decode --edition=2021 tests/decode.rs --error-format=json --json=diagnostic-rendered-ansi,artifacts,future-incompat --emit=dep-info,link -C embed-bitcode=no -C debuginfo=2 --test --check-cfg 'cfg(docsrs,test)' --check-cfg 'cfg(feature, values("_benchmarks"))' -C metadata=67c26e46da547f56 -C extra-filename=-c860889ae0ce7648 --out-dir /home/runner/work/image-webp/image-webp/target/debug/deps -L dependency=/home/runner/work/image-webp/image-webp/target/debug/deps --extern byteorder_lite=/home/runner/work/image-webp/image-webp/target/debug/deps/libbyteorder_lite-a278a9f14042f35b.rlib --extern image_webp=/home/runner/work/image-webp/image-webp/target/debug/deps/libimage_webp-c2294830a6b5f4a4.rlib --extern paste=/home/runner/work/image-webp/image-webp/target/debug/deps/libpaste-594f55fe5cfdc9fd.so --extern png=/home/runner/work/image-webp/image-webp/target/debug/deps/libpng-e598a91edf8375c4.rlib --extern quick_error=/home/runner/work/image-webp/image-webp/target/debug/deps/libquick_error-d88c5aeea3a3d7d1.rlib --extern rand=/home/runner/work/image-webp/image-webp/target/debug/deps/librand-afaa0a85c24cc4e5.rlib --extern webp=/home/runner/work/image-webp/image-webp/target/debug/deps/libwebp-7648140fa8b53cb3.rlib -L native=/home/runner/work/image-webp/image-webp/target/debug/build/libwebp-sys-7669b733598afc52/out -L native=/home/runner/work/image-webp/image-webp/target/debug/build/libwebp-sys-7669b733598afc52/out`
[1m[92m    Finished[0m `test` profile [unoptimized + debuginfo] target(s) in 15.97s
[1m[92m     Running[0m `/home/runner/work/image-webp/image-webp/target/debug/deps/image_webp-5a4d9592037bd063`

running 33 tests
test alpha_blending::tests::alpha_blending_optimization ... ignored
test decoder::tests::add_with_overflow_size ... ok
test decoder::tests::decode_2x2_single_color_image ... ok
test decoder::tests::decode_3x3_single_color_image ... ok
test extended::tests::binary_alpha_blend_selects_exact_pixel ... ok
test extended::tests::dispose_clear_fullsize_rgb_frame ... ok
test extended::tests::dispose_clear_subframe_rgb_frame ... ok
test extended::tests::reconstruct_alpha_filters ... ok
test lossless::decoder::test::bit_read_error_test ... ok
test lossless::decoder::test::bit_read_test ... ok
test lossy::arithmetic_decoder::tests::test_arithmetic_decoder_hello_long ... ok
test lossy::arithmetic_decoder::tests::test_arithmetic_decoder_hello_short ... ok
test lossy::arithmetic_decoder::tests::test_arithmetic_decoder_uninit ... ok
test lossy::arithmetic_encoder::tests::test_arithmetic_encoder_hello ... ok
test lossy::arithmetic_encoder::tests::test_arithmetic_encoder_short ... ok
test lossy::arithmetic_encoder::tests::test_encoder_tree ... ok
test lossy::arithmetic_encoder::tests::test_encoder_with_decoder ... ok
test lossy::prediction::tests::test_add_residue ... ok
test lossy::prediction::tests::test_avg2 ... ok
test lossy::prediction::tests::test_avg2_specific ... ok
test encoder::tests::write_webp ... ok
test lossy::prediction::tests::test_edge_pixels ... ok
test lossy::prediction::tests::test_predict_bhepred ... ok
test lossy::prediction::tests::test_predict_bldpred ... ok
test lossy::prediction::tests::test_predict_brdpred ... ok
test lossy::prediction::tests::test_predict_bvepred ... ok
test lossy::prediction::tests::test_top_pixels ... ok
test lossy::transform::tests::test_dct_inverse ... ok
test encoder::tests::write_webp_exif ... ok
test lossy::yuv::tests::test_fancy_grid ... ok
test lossy::yuv::tests::test_yuv_conversions ... ok
test encoder::tests::roundtrip_libwebp ... ok
test lossy::prediction::tests::test_avg3 ... ok

test result: ok. 32 passed; 0 failed; 1 ignored; 0 measured; 0 filtered out; finished in 0.62s

[1m[92m     Running[0m `/home/runner/work/image-webp/image-webp/target/debug/deps/decode-c860889ae0ce7648`

running 31 tests
test reftest_animated_random_lossless ... ok
test reftest_animated_random_lossy ... ok
test reftest_gallery1_1 ... ok
test reftest_gallery1_2 ... ok
test reftest_gallery2_1_webp_a ... ok
test reftest_gallery2_1_webp_ll ... ok
test reftest_gallery2_2_webp_a ... ok
test reftest_gallery2_2_webp_ll ... ok
test reftest_gallery1_4 ... ok
test reftest_gallery1_5 ... ok
test reftest_gallery1_3 ... ok
test reftest_gallery2_4_webp_a ... ok
test reftest_gallery2_4_webp_ll ... ok
test reftest_gallery2_5_webp_ll ... ok
test reftest_gallery2_3_webp_ll ... ok
test reftest_gallery2_5_webp_a ... ok
test reftest_gallery2_3_webp_a ... ok
test reftest_nofancy_gallery1_1 ... ok
test reftest_nofancy_gallery1_2 ... ok
test reftest_regression_color_index ... ok
test reftest_regression_dark ... ok
test reftest_regression_lossless_indexed_1bit_palette ... ok
test reftest_regression_lossless_indexed_2bit_palette ... ok
test reftest_regression_lossless_indexed_4bit_palette ... ok
test reftest_regression_tiny ... ok
test test_vp8l_max_height_dimensions ... ok
test test_vp8l_max_width_and_height_dimensions ... ok
test test_vp8l_max_width_dimensions ... ok
test reftest_nofancy_gallery1_4 ... ok
test reftest_nofancy_gallery1_5 ... ok
test reftest_nofancy_gallery1_3 ... ok

test result: ok. 31 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 2.13s

[1m[92m   Doc-tests[0m image_webp
[1m[92m     Running[0m `/home/runner/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/bin/rustdoc --edition=2021 --crate-type lib --color always --crate-name image_webp --test src/lib.rs --test-run-directory /home/runner/work/image-webp/image-webp -L native=/home/runner/work/image-webp/image-webp/target/debug/build/libwebp-sys-7669b733598afc52/out --extern byteorder_lite=/home/runner/work/image-webp/image-webp/target/debug/deps/libbyteorder_lite-a278a9f14042f35b.rlib --extern image_webp=/home/runner/work/image-webp/image-webp/target/debug/deps/libimage_webp-c2294830a6b5f4a4.rlib --extern paste=/home/runner/work/image-webp/image-webp/target/debug/deps/libpaste-594f55fe5cfdc9fd.so --extern png=/home/runner/work/image-webp/image-webp/target/debug/deps/libpng-e598a91edf8375c4.rlib --extern quick_error=/home/runner/work/image-webp/image-webp/target/debug/deps/libquick_error-d88c5aeea3a3d7d1.rlib --extern rand=/home/runner/work/image-webp/image-webp/target/debug/deps/librand-afaa0a85c24cc4e5.rlib --extern webp=/home/runner/work/image-webp/image-webp/target/debug/deps/libwebp-7648140fa8b53cb3.rlib -L dependency=/home/runner/work/image-webp/image-webp/target/debug/deps -C embed-bitcode=no --check-cfg 'cfg(docsrs,test)' --check-cfg 'cfg(feature, values("_benchmarks"))' --error-format human`

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

```

## Clippy tail
```text
[1m[92m    Checking[0m quick-error v2.0.1
[1m[92m    Checking[0m byteorder-lite v0.1.0
[1m[92m    Checking[0m image-webp v0.2.4 (/home/runner/work/image-webp/image-webp)
[1m[92m    Finished[0m `dev` profile [unoptimized + debuginfo] target(s) in 0.87s
```

## MSRV tail
```text
[1m[32m    Updating[0m crates.io index
[1m[32m Downloading[0m crates ...
[1m[32m  Downloaded[0m quick-error v2.0.1
[1m[32m  Downloaded[0m byteorder-lite v0.1.0
[1m[32m   Compiling[0m quick-error v2.0.1
[1m[32m   Compiling[0m byteorder-lite v0.1.0
[1m[32m     Running[0m `/home/runner/.rustup/toolchains/1.80.1-x86_64-unknown-linux-gnu/bin/rustc --crate-name quick_error --edition=2018 /home/runner/.cargo/registry/src/index.crates.io-6f17d22bba15001f/quick-error-2.0.1/src/lib.rs --error-format=json --json=diagnostic-rendered-ansi,artifacts,future-incompat --crate-type lib --emit=dep-info,metadata,link -C embed-bitcode=no -C debuginfo=2 --check-cfg 'cfg(docsrs)' --check-cfg 'cfg(feature, values())' -C metadata=05f97fef35249ec6 -C extra-filename=-05f97fef35249ec6 --out-dir /home/runner/work/image-webp/image-webp/target/debug/deps -L dependency=/home/runner/work/image-webp/image-webp/target/debug/deps --cap-lints allow`
[1m[32m     Running[0m `/home/runner/.rustup/toolchains/1.80.1-x86_64-unknown-linux-gnu/bin/rustc --crate-name byteorder_lite --edition=2021 /home/runner/.cargo/registry/src/index.crates.io-6f17d22bba15001f/byteorder-lite-0.1.0/src/lib.rs --error-format=json --json=diagnostic-rendered-ansi,artifacts,future-incompat --crate-type lib --emit=dep-info,metadata,link -C embed-bitcode=no -C debuginfo=2 --cfg 'feature="default"' --cfg 'feature="std"' --check-cfg 'cfg(docsrs)' --check-cfg 'cfg(feature, values("default", "std"))' -C metadata=225adb4ca8161e46 -C extra-filename=-225adb4ca8161e46 --out-dir /home/runner/work/image-webp/image-webp/target/debug/deps -L dependency=/home/runner/work/image-webp/image-webp/target/debug/deps --cap-lints allow`
[1m[32m   Compiling[0m image-webp v0.2.4 (/home/runner/work/image-webp/image-webp)
[1m[32m     Running[0m `/home/runner/.rustup/toolchains/1.80.1-x86_64-unknown-linux-gnu/bin/rustc --crate-name image_webp --edition=2021 src/lib.rs --error-format=json --json=diagnostic-rendered-ansi,artifacts,future-incompat --crate-type lib --emit=dep-info,metadata,link -C embed-bitcode=no -C debuginfo=2 --check-cfg 'cfg(docsrs)' --check-cfg 'cfg(feature, values("_benchmarks"))' -C metadata=57893f2a5355531b -C extra-filename=-57893f2a5355531b --out-dir /home/runner/work/image-webp/image-webp/target/debug/deps -L dependency=/home/runner/work/image-webp/image-webp/target/debug/deps --extern byteorder_lite=/home/runner/work/image-webp/image-webp/target/debug/deps/libbyteorder_lite-225adb4ca8161e46.rmeta --extern quick_error=/home/runner/work/image-webp/image-webp/target/debug/deps/libquick_error-05f97fef35249ec6.rmeta`
[1m[32m    Finished[0m `dev` profile [unoptimized + debuginfo] target(s) in 1.40s
```

## Candidate diff
```diff
diff --git a/src/lossy/arithmetic_decoder.rs b/src/lossy/arithmetic_decoder.rs
index 50db0f5..6fabc84 100644
--- a/src/lossy/arithmetic_decoder.rs
+++ b/src/lossy/arithmetic_decoder.rs
@@ -205,6 +205,18 @@ impl ArithmeticDecoder {
         self.cold_read_optional_signed_value(n)
     }
 
+    #[inline(never)]
+    pub(crate) fn read_dct_token(
+        &mut self,
+        tree: &[TreeNode; 11],
+        skip_eob: bool,
+    ) -> BitResult<i8> {
+        if let Some(v) = self.fast().read_dct_token(tree, skip_eob) {
+            return BitResult::ok(v);
+        }
+        self.cold_read_with_tree(tree, skip_eob as usize)
+    }
+
     // This is generic and inlined just to skip the first bounds check.
     #[inline]
     pub(crate) fn read_with_tree<const N: usize>(&mut self, tree: &[TreeNode; N]) -> BitResult<i8> {
@@ -435,6 +447,11 @@ impl FastDecoder<'_> {
         self.commit_if_valid(value)
     }
 
+    fn read_dct_token(mut self, tree: &[TreeNode; 11], skip_eob: bool) -> Option<i8> {
+        let value = self.fast_read_dct_token(tree, skip_eob);
+        self.commit_if_valid(value)
+    }
+
     fn read_with_tree(mut self, tree: &[TreeNode], first_node: TreeNode) -> Option<i8> {
         let value = self.fast_read_with_tree(tree, first_node);
         self.commit_if_valid(value)
@@ -616,6 +633,51 @@ impl FastDecoder<'_> {
         v
     }
 
+    fn fast_read_dct_token(&mut self, tree: &[TreeNode; 11], skip_eob: bool) -> i8 {
+        if !skip_eob && !self.fast_read_bit(tree[0].prob) {
+            return TreeNode::value_from_branch(tree[0].left);
+        }
+        if !self.fast_read_bit(tree[1].prob) {
+            return TreeNode::value_from_branch(tree[1].left);
+        }
+        if !self.fast_read_bit(tree[2].prob) {
+            return TreeNode::value_from_branch(tree[2].left);
+        }
+        if !self.fast_read_bit(tree[3].prob) {
+            if !self.fast_read_bit(tree[4].prob) {
+                return TreeNode::value_from_branch(tree[4].left);
+            }
+            let n = tree[5];
+            return TreeNode::value_from_branch(if self.fast_read_bit(n.prob) {
+                n.right
+            } else {
+                n.left
+            });
+        }
+        if !self.fast_read_bit(tree[6].prob) {
+            let n = tree[7];
+            return TreeNode::value_from_branch(if self.fast_read_bit(n.prob) {
+                n.right
+            } else {
+                n.left
+            });
+        }
+        if !self.fast_read_bit(tree[8].prob) {
+            let n = tree[9];
+            return TreeNode::value_from_branch(if self.fast_read_bit(n.prob) {
+                n.right
+            } else {
+                n.left
+            });
+        }
+        let n = tree[10];
+        TreeNode::value_from_branch(if self.fast_read_bit(n.prob) {
+            n.right
+        } else {
+            n.left
+        })
+    }
+
     fn fast_read_with_tree(&mut self, tree: &[TreeNode], mut node: TreeNode) -> i8 {
         loop {
             let prob = node.prob;
diff --git a/src/lossy/mod.rs b/src/lossy/mod.rs
index 9bb46e6..beaf152 100644
--- a/src/lossy/mod.rs
+++ b/src/lossy/mod.rs
@@ -813,9 +813,7 @@ impl<R: Read> Vp8Decoder<R> {
             let band = COEFF_BANDS[i] as usize;
             let tree = &probs[band][complexity];
 
-            let token = decoder
-                .read_with_tree_with_first_node(tree, tree[skip as usize])
-                .or_accumulate(&mut res);
+            let token = decoder.read_dct_token(tree, skip).or_accumulate(&mut res);
 
             let mut abs_value = i32::from(match token {
                 DCT_EOB => break,

```
